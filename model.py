"""
model.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from typing import Any
from agents import Person
from mesa import Model
from mesa.discrete_space import HexGrid
from mesa.space import PropertyLayer
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
        self.generator = random.Random()
        self.generator.seed(seed)
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
        self.grid = HexGrid(dimensions = [height,width], torus = False, random=self.generator)
        self.generateTileFertility()
        self.assignAgents(agentCount)

    # Set the fertility of each individual tile, starting with the river.
    def generateTileFertility(self):
        # Prepare to instantiate fertility values by creating
        # an empty property layer
        fertilityField = self.grid.create_property_layer("Fertility", 0)
        # Place the river's first tile
        j = int(self.height/2)
        fertilityField.data[j][0] = self.e7RiverFertilityValue
        #Place the rest of the river in order
        for i in range(1, self.width):
            if j > 0 and j < self.height - 1:
                j = self.random.randint(j-1,j+1)
            elif j > 0:
                j = self.random.randint(j-1, j)
            else:
                j = self.random.randint(j, j+1)
            fertilityField.data[j][i] = self.e7RiverFertilityValue
        # Diffuse fertility across the grid
        fertilityField.data = self.diffuseValues(fertilityField.data)
    
    # Diffuse fertility from the river valley using a recursive methadology
    def diffuseValues(self, array2d):
        # initialize a new array with the same dimensions:
        newArray = [[0.0 for _ in range(0,self.height)] for _ in range(0, self.width)]
        # if there are no zeroes in the resulting matrix, we have successfully diffused the entire map, and can return
        noZeroes = True
        for row in range(0, self.width):
            for column in range(0, self.height):
                # If a value already exists for a given location, keep it!
                if array2d[row][column] != 0:
                    newArray[row][column] = array2d[row][column]
                # Otherwise, diffuse from adjacent hexes
                else:
                    adjacencies = []
                    for i in range(row-1, row+2):
                        for j in range(column-1, column+2):
                            if i >= 0 and i < self.height and j >= 0 and j < self.width:
                                adjacencies.append(array2d[i][j])
                    newArray[row][column] = (sum(adjacencies))/len(adjacencies)
                    if newArray[row][column] == 0:
                        noZeroes = False
        if noZeroes:
            return newArray
        return self.diffuseValues(newArray)


    # Provide the initial assignments of agents to tiles
    def assignAgents(self, count):
        # Randomly assign agents to tiles
        Person.create_agents(
            self,
            count,
            self.random.choices(self.grid.all_cells.cells, k=count),
            lifeExpectancy = self.rng.integers(45,76, count),
            e4ReproductionFraction = self.e4ReproductionFraction,
            e5DeathThreshold = self.e5DeathThreshold,
            e6ReproductionThreshold = self.e6ReproductionThreshold,
        )

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
        self.agents.do("ageUpdates")
        self.agents.do("updatePreference")
        self.calculateTileYields()
        self.feedAgents()
        self.agents.do("reproduction")
        self.updateTiles()
        self.agents.do("move")