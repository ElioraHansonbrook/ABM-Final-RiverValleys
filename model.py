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
                e1FarmedPortionPerPerson: float,
                e2FarmingDecayRate: float,
                e3InfrastructureDecayRate: float,
                e4ReproductionFraction: float,
                e5DeathThreshold: float,
                e6ReproductionThreshold: float,
                c1InitialClimateLowerThreshold: float,
                c2InitialClimateUpperThreshold: float,
                c3DisruptionClimateLowerThreshold: float,
                c4DisruptionClimateUpperThreshold: float,
                ) -> None:
        super().__init__(*args, seed=seed, rng=rng, scenario=scenario,)
        self.height = height
        self.width = width
        self.e1FarmedPortionPerPerson = e1FarmedPortionPerPerson
        self.e2FarmingDecayRate = e2FarmingDecayRate
        self.e3InfrastructureDecayRate = e3InfrastructureDecayRate
        self.e4ReproductionFraction = e4ReproductionFraction
        self.e5DeathThreshold = e5DeathThreshold
        self.e6ReproductionThreshold = e6ReproductionThreshold
        self.c1InitialClimateLowerThreshold = c1InitialClimateLowerThreshold
        self.c2InitialClimateUpperThreshold = c2InitialClimateUpperThreshold
        self.c3DisruptionClimateLowerThreshold = c3DisruptionClimateLowerThreshold
        self.c4DisruptionClimateUpperThreshold = c4DisruptionClimateUpperThreshold
        self.grid = HexMultiGrid(width = width, height = height, torus = False)
        self.generateTileFertility(0) #FIX AND REPLACE WITH GENERATOR
        self.assignAgents(agentCount)

    # Set the fertility of each individual tile, starting with the river.
    def generateTileFertility(self, generator):
        pass

    # Provide the initial assignments of agents to tiles
    def assignAgents(self, count):
        pass

    # Set the total possible yields for a tile in the given round
    def calculateTileYields(self):
        pass

    # Assign food to agents on each tile, based on agent preferences and food availability
    def feedAgents(self):
        pass

    # Update the infrastructure and farmed proportions on each tile.
    def updateTiles(self):
        pass

    # A single step of the model
    def step(self):
        self.agents.do("updatePreference")
        self.calculateTileYields()
        self.feedAgents()
        self.agents.do("reproduction")
        self.updateTiles()
        self.agents.do("move")