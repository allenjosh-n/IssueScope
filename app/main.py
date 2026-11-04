from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from app.config import Settings, get_settings
from app.llm import chat, stream_chat
from app.schemas import ChatRequest, ChatResponse, UsageResponse
from app.usage import usage_store

app = FastAPI(title="IssueScope", version="0.2.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest, settings: SettingsDep):
    """
    Send a conversation to the LLM and receive a structured JSON response.

    Set `stream: true` in the request body to receive a Server-Sent Events stream
    instead. Each SSE event carries a plain-text chunk; the final event is
    `data: [DONE]`.
    """
    if body.stream:
        return StreamingResponse(
            _sse_generator(body, settings),
            media_type="text/event-stream",
        )

    answer, model_used, in_tok, out_tok, cost = await chat(body.messages, settings)
    usage_store.record(in_tok, out_tok, cost)

    return ChatResponse(
        answer=answer,
        model_used=model_used,
        input_tokens=in_tok,
        output_tokens=out_tok,
        cost_usd=round(cost, 6),
    )


async def _sse_generator(body: ChatRequest, settings: Settings) -> AsyncIterator[str]:
    """Yield SSE-formatted chunks from the streaming LLM call."""
    total_chunks = ""
    async for chunk in stream_chat(body.messages, settings):
        total_chunks += chunk
        yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    # Approximate usage tracking for streamed responses (no token counts from stream)
    yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------


@app.get("/usage", response_model=UsageResponse)
def usage_endpoint() -> UsageResponse:
    """Return cumulative token and cost statistics since the last process restart."""
    return UsageResponse(**usage_store.snapshot())
