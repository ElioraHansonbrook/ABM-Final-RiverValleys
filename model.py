from typing import Any

from mesa import Model
from mesa.space import HexMultiGrid
#IMPORT RANDOM GENERATOR

# A model of a river valley
class RiverValley(Model):
    def __init__(self,
                *args: Any,
                seed: float | None = None,
                rng: int | None = None,
                scenario: Any | None = None,
                height: int = 5,
                width: int = 5,
                agentCount: int = 25,
                ) -> None:
        super().__init__(*args, seed=seed, rng=rng, scenario=scenario,)
        self.height = height
        self.width = width
        self.grid = HexMultiGrid(width = width, height = height, torus = False)
        self.generateTileFertility(0) #FIX AND REPLACE WITH GENERATOR
        self.assignAgents(agentCount)

    # Set the fertility of each individual tile, surrounding the river.
    def generateTileFertility(self, generator):
        pass

    # Provide the initial assignments of agents to tiles
    def assignAgents(self, count):
        pass

    # A single step of the model
    def step(self):
        pass

#Test sequence
if __name__ == "__main__":
    model = RiverValley(height=5, width=5)