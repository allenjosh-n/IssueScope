"""LLM client with fallback, retry, and timeout logic."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from openai import APIStatusError, APITimeoutError, AsyncOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import Settings
from app.schemas import Message

logger = logging.getLogger(__name__)

# Exceptions that are worth retrying on the same model before trying the fallback.
_RETRYABLE = (APITimeoutError,)


def _cost(input_tokens: int, output_tokens: int, cost_in: float, cost_out: float) -> float:
    return (input_tokens / 1000) * cost_in + (output_tokens / 1000) * cost_out


async def _call_model(
    client: AsyncOpenAI,
    model: str,
    messages: list[dict],
    timeout: float,
) -> tuple[str, int, int]:
    """Call a single model and return (answer, input_tokens, output_tokens)."""

    @retry(
        retry=retry_if_exception_type(_RETRYABLE),
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        reraise=True,
    )
    async def _inner() -> tuple[str, int, int]:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            timeout=timeout,
        )
        choice = response.choices[0]
        usage = response.usage
        return (
            choice.message.content or "",
            usage.prompt_tokens if usage else 0,
            usage.completion_tokens if usage else 0,
        )

    return await _inner()


async def chat(
    messages: list[Message],
    settings: Settings,
) -> tuple[str, str, int, int, float]:
    """
    Send messages to the primary model, falling back to the secondary model on
    timeout or 5xx errors.

    Returns:
        (answer, model_used, input_tokens, output_tokens, cost_usd)
    """
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    payload = [{"role": m.role, "content": m.content} for m in messages]

    model = settings.openai_model
    cost_in = settings.primary_cost_per_1k_input
    cost_out = settings.primary_cost_per_1k_output

    try:
        answer, in_tok, out_tok = await _call_model(client, model, payload, timeout=15.0)
    except (APITimeoutError, APIStatusError) as exc:
        logger.warning("Primary model %s failed (%s), trying fallback.", model, exc)
        model = settings.fallback_model
        cost_in = settings.fallback_cost_per_1k_input
        cost_out = settings.fallback_cost_per_1k_output
        answer, in_tok, out_tok = await _call_model(client, model, payload, timeout=20.0)

    return answer, model, in_tok, out_tok, _cost(in_tok, out_tok, cost_in, cost_out)


async def stream_chat(
    messages: list[Message],
    settings: Settings,
) -> AsyncIterator[str]:
    """
    Stream tokens from the primary model, falling back on the first error.
    Yields raw text chunks. Caller is responsible for SSE formatting.
    """
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    payload = [{"role": m.role, "content": m.content} for m in messages]

    models_to_try = [settings.openai_model, settings.fallback_model]

    for model in models_to_try:
        try:
            async with client.chat.completions.stream(
                model=model,
                messages=payload,  # type: ignore[arg-type]
                timeout=20.0,
            ) as stream:
                async for event in stream:
                    delta = event.choices[0].delta.content if event.choices else None
                    if delta:
                        yield delta
            return  # success — stop after first working model
        except (APITimeoutError, APIStatusError) as exc:
            logger.warning("Streaming model %s failed (%s), trying next.", model, exc)
            continue

    raise RuntimeError("All models failed during streaming.")
