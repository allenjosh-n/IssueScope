"""Request and response schemas for IssueScope API."""

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# /chat
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str = Field(..., examples=["user", "assistant", "system"])
    content: str


class ChatRequest(BaseModel):
    messages: list[Message] = Field(
        ...,
        min_length=1,
        description="Conversation history. Last message must be from the user.",
    )
    stream: bool = Field(False, description="If true, return a Server-Sent Events stream.")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="The assistant's reply.")
    model_used: str = Field(..., description="Which model produced this response.")
    input_tokens: int
    output_tokens: int
    cost_usd: float = Field(..., description="Estimated cost in USD for this request.")


# ---------------------------------------------------------------------------
# /usage
# ---------------------------------------------------------------------------

class UsageResponse(BaseModel):
    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_cost_usd: float = Field(..., description="Cumulative cost in USD since last restart.")
