"""In-memory usage tracker. Resets on process restart.

For a persistent store, replace the dataclass with DB writes in Week 3.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass
class _UsageStore:
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    def record(self, input_tokens: int, output_tokens: int, cost_usd: float) -> None:
        with self._lock:
            self.total_requests += 1
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_cost_usd += cost_usd

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "total_requests": self.total_requests,
                "total_input_tokens": self.total_input_tokens,
                "total_output_tokens": self.total_output_tokens,
                "total_cost_usd": round(self.total_cost_usd, 6),
            }


# Module-level singleton — imported by main.py
usage_store = _UsageStore()
