"""The levers. Every run is fully described by one RunConfig; same config + seed = same export."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal


class RunConfig(BaseModel):
    seed: int = 42
    start: str = "2025-09-01"
    end: str = "2026-08-31"
    format: Literal["square", "toast"] = "toast"

    # Scale
    annual_sales: float = Field(1_100_000, gt=0, description="target annual net sales, before noise (research default $1.1M; range $0.6-1.8M)")

    # Randomness
    noise: float = Field(0.10, ge=0, le=0.5, description="day-to-day noise, CV of a log-normal draw per day")
    effect_jitter: float = Field(0.3, ge=0, le=1, description="how far each effect may land from the research midpoint, as a fraction of the range")
    zero_chance: float = Field(0.25, ge=0, le=1, description="probability that any given optional effect is switched off this year")

    # Wildcards
    wildcards: int = Field(2, ge=0, le=6)
    wildcard_intensity: Literal["low", "medium", "high"] = "medium"

    # Restaurant shape: blind = the code picks and seals it
    blind_shape: bool = True
    hours_profile: Literal["standard", "late-bar", "brunch", "closed-monday"] | None = None   # ignored when blind
    patio: bool | None = None
    bar: bool | None = None

    # Flavor (LLM): off = built-in defaults
    llm: bool = False
    llm_model: str = "claude-sonnet-4-5"

    out_dir: str = "runs"
