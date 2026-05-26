"""
model.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from typing import Any

from mesa import Model
from mesa.space import HexMultiGrid
import random

# A model of a river valley
class RiverValley(Model):
    def __init__(self,
                seed = None,
                height = 5,
                width = 5,
                agentCount = 25,
                e1FarmedPortionPerPerson = 50,
                e2FarmingDecayRate = 10,
                e3InfrastructureDecayRate = 10,
                e4ReproductionFraction = 10,
                e5DeathThreshold = 5,
                e6ReproductionThreshold = 15,
                e7RiverFertilityValue = 1,
                c1InitialClimateLowerThreshold = 30,
                c2InitialClimateUpperThreshold = 34,
                c3DisruptionClimateLowerThreshold = 14,
                c4DisruptionClimateUpperThreshold = 24,
                ) -> None:
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.e1FarmedPortionPerPerson = e1FarmedPortionPerPerson
        self.e2FarmingDecayRate = e2FarmingDecayRate
        self.e3InfrastructureDecayRate = e3InfrastructureDecayRate
        self.e4ReproductionFraction = e4ReproductionFraction
        self.e5DeathThreshold = e5DeathThreshold
        self.e6ReproductionThreshold = e6ReproductionThreshold
        self.e7RiverFertilityValue = e7RiverFertilityValue
        self.c1InitialClimateLowerThreshold = c1InitialClimateLowerThreshold
        self.c2InitialClimateUpperThreshold = c2InitialClimateUpperThreshold
        self.c3DisruptionClimateLowerThreshold = c3DisruptionClimateLowerThreshold
        self.c4DisruptionClimateUpperThreshold = c4DisruptionClimateUpperThreshold
        self.grid = HexMultiGrid(width = width, height = height, torus = False)
        self.generateTileFertility(0) #FIX AND REPLACE WITH GENERATOR
        self.assignAgents(agentCount)

    # Set the fertility of each individual tile, starting with the river.
    def generateTileFertility(self, generator):
        random.seed(generator)
        # Prepare to instantiate fertility values by creating
        # a two dimensional array stacked with nil values
        fertilityField = []
        for _ in range(self.width):
            column = []
            for _ in range(self.height):
                column.append(None)
            fertilityField.append(column)
        # Place the river
        j = random.randint(0,self.height-1)
        fertilityField[0][j] = self.e7RiverFertilityValue
        for i in range(1, self.width):
            if j > 0 and j < self.height - 1:
                j = random.randint(j-1,j+1)
            elif j > 0:
                j = random.randint(j-1, j)
            else:
                j = random.randint(j, j+1)
            fertilityField[i][j] = 1
        # Update fertility around the river
        # while None in fertilityField:
        #     for array in fertilityField:
        #         for value in array:
        #             pass


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