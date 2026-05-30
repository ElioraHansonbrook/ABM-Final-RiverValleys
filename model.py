"""
model.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from typing import Any, cast
from agents import Person
from mesa import Model, DataCollector
import math
from mesa.discrete_space import HexGrid
from mesa.discrete_space import Grid
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
                c5DisruptionStartTurn = 500,
                c6DisruptionEndTurn = 525,
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
        self.c5DisruptionStartTurn = c5DisruptionStartTurn
        self.c6DisruptionEndTurn = c6DisruptionEndTurn
        self.turn = 0
        self.grid = HexGrid(dimensions = [height,width], torus = False, random=self.generator)
        self.generateTileFertility()
        self.finishTileGeneration()
        self.assignAgents(agentCount)
        self.datacollector = DataCollector(
            {"Population": lambda _: len(self.agents)}
        )

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

    # Add all other values to each tile.
    def finishTileGeneration(self):
        self.grid.create_property_layer("TotalYield", 0)
        self.grid.create_property_layer("PreviousYield", 0)
        self.grid.create_property_layer("HGYield", 0)
        self.grid.create_property_layer("AgYield", 0)
        self.grid.create_property_layer("FarmingProportion", 0)
        self.grid.create_property_layer("Infrastructure", 0)
        self.grid.create_property_layer("FarmingUtilized", 0)
        self.grid.create_property_layer("IndividualAgYield", 0)
        self.grid.create_property_layer("IndividualHGYield", 0)
        self.grid.create_property_layer("Population", 0)

    # Provide the initial assignments of agents to tiles
    def assignAgents(self, count):
        # Randomly assign agents to tiles
        Person.create_agents(
            self,
            count,
            self.random.choices(self.grid.all_cells.cells, k=count),
            lifeExpectancy = self.rng.integers(45,76, count),
            # These three values need to be passed down to agents because there's an issue with
            # circular imports not being permitted in Python.
            e4ReproductionFraction = self.e4ReproductionFraction,
            e5DeathThreshold = self.e5DeathThreshold,
            e6ReproductionThreshold = self.e6ReproductionThreshold,
        )


    # Set the total possible yields for a tile in the given round
    def calculateTileYields(self):
        # Calculate overall climate value
        if self.turn < self.c5DisruptionStartTurn or self.turn >= self.c6DisruptionEndTurn:
            climate = self.random.randint(self.c1InitialClimateLowerThreshold, self.c2InitialClimateUpperThreshold + 1)
        else:
            climate = self.random.randint(self.c3DisruptionClimateLowerThreshold, self.c4DisruptionClimateUpperThreshold + 1)
        # Apply the climate to each cell to calculate the cells' yields for the upcoming turn
        for cell in self.grid._celllist:
            cell.TotalYield = cell.Fertility * climate + climate
            cell.HGYield = max(cell.TotalYield * (1-cell.FarmingProportion), 0)
            cell.AgYield = max(cell.TotalYield * cell.FarmingProportion * (1 + cell.Infrastructure) - abs(cell.PreviousYield - cell.TotalYield), 0)
            cell.Population = len(cell._agents)
            cell.PreviousYield = cell.TotalYield

    # Assign food to agents on each tile, based on agent preferences and food availability
    def feedAgents(self):
        # Feed the agents in each cell
        for cell in self.grid._celllist:
            # Accumulator pattern to get the total preference of all agents on a tile
            totalPreference = (0.0,0.0)
            for agent in cell.agents:
                cast(Person, agent)
                totalPreference = (totalPreference[0] + agent.preference[0], totalPreference[1] + agent.preference[1])
            # Update farming utilization for this tile; this is needed to calculate the farming proportion of the tile later on
            if totalPreference[0] + totalPreference[1] > 0: #Just to prevent Db0 Error
                # Min *probably* doesn't do anything here, but I was getting a weird bug earlier so I added it just to be safe
                cell.FarmingUtilized = min(totalPreference[1] * 1/self.e1FarmedPortionPerPerson, 1.0)
            else:
                cell.FarmingUtilized = 0
            # Now that that's all done, the agents get fed:
            for agent in cell.agents:
                cast(Person, agent)
                # Feed one agent
                agent.food = (agent.preference[0]/totalPreference[0]*cell.HGYield, agent.preference[1]/totalPreference[1]*cell.AgYield)
            # Calculate the average yields per agent for the tile; this is just to help agents know where to move later on, but
            # it also makes a nice visualization as an added bonus.
            if totalPreference[0] > 0: #Just to prevent Db0 Error
                cell.IndividualHGYield = 1/totalPreference[0]*cell.HGYield
            else:
                cell.IndividualHGYield = cell.HGYield
            if totalPreference[1] > 0: #Just to prevent Db0 Error
                cell.IndividualAgYield = max(1/totalPreference[1]*cell.AgYield, 0)
            else:
                cell.IndividualAgYield = cell.AgYield

    # Update the infrastructure and farmed proportions on each tile.
    def updateTiles(self):
        for cell in self.grid._celllist:
            # Update infrastructure as specified in model
            cell.Infrastructure = abs(cell.Infrastructure/self.e3InfrastructureDecayRate) + math.log(1 + cell.FarmingProportion * cell.Population + 0.02 * cell.Population, self.e2FarmingDecayRate)
            # Update how much of the cell is currently converted to farmland; this impacts future farming and hunter-gatherer yields.
            if cell.FarmingUtilized > cell.FarmingProportion:
                cell.FarmingProportion = cell.FarmingUtilized
            else:
                cell.FarmingProportion = min(cell.FarmingProportion - abs(cell.FarmingUtilized - cell.FarmingProportion) / self.e2FarmingDecayRate, 1.0)

    # A single step of the model
    def step(self):
        self.turn += 1
        self.agents.do("ageUpdates")
        self.agents.do("updatePreference")
        self.calculateTileYields()
        self.feedAgents()
        self.agents.do("reproduction")
        self.updateTiles()
        self.agents.do("move")
        self.datacollector.collect(self)
        # for agent in self.agents:
        #     cast(Person, agent)
        #     print(agent.preference)