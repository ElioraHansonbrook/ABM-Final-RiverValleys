from typing import Any

from mesa import Model

class RiverValley(Model):
    def __init__(self, *args: Any, seed: float | None = None, rng: Generator | BitGenerator | int | integer[Any] | Sequence[int] | SeedSequence | None = None, scenario: Any | None = None, **kwargs: Any) -> None:
        super().__init__(*args, seed=seed, rng=rng, scenario=scenario, **kwargs)