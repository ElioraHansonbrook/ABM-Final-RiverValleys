"""
agents.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from mesa.discrete_space import CellAgent, Cell

class Person(CellAgent):
    def __init__(self,
                model: model,
                cell,
                preference = (0.1, 0.9), # Food acquisition preference
                age = 0,
                lifeExpectancy = 80,
                e4ReproductionFraction = 10,
                e5DeathThreshold = 5,
                e6ReproductionThreshold = 15,
                *args,
                **kwargs) -> None:
        super().__init__(model, *args, **kwargs)
        self.preference = preference
        self.age = age
        self.lifeExpectancy = lifeExpectancy
        self.cell = cell
        self.e4ReproductionFraction = e4ReproductionFraction
        self.e5DeathThreshold = e5DeathThreshold
        self.e6ReproductionThreshold = e6ReproductionThreshold
        self.food = (0,0)

    # Update the age of the agent, and kill if needed
    def ageUpdates(self):
        self.age += 1
        if self.age >= self.lifeExpectancy:
            self.remove()
    
    # Update the preference of the model as the first step in a round.
    def updatePreference(self):
        # Only try to update when some food was gathered to prevent divide by zero errors
        if self.food[0] + self.food[1] != 0:
            updatedPreference = ((self.preference[0] + (self.food[0]/(self.food[0] + self.food[1])))/2,
                             (self.preference[1] + (self.food[1]/(self.food[0] + self.food[1])))/2)
            self.preference = updatedPreference
    
    # Confirm the agent doesn't starve to death; Attempt reproduction, if requirements are met
    def reproduction(self):
        totalFood = self.food[0] + self.food[1]
        bonus = 3 if self.age < 18 or self.age > 45 else 0
        if totalFood < self.e5DeathThreshold + bonus:
            self.remove()
        if totalFood > self.e6ReproductionThreshold:
            if self.age >= 18 and self.age <= 45 and self.random.randint(0,self.e4ReproductionFraction) == 0:
                Person.create_agents(
                    self.model,
                    1,
                    cell = self.cell,
                    preference = self.preference,
                    age = 0,
                    lifeExpectancy = self.random.randint(45,76),
                    e4ReproductionFraction = self.e4ReproductionFraction,
                    e5DeathThreshold = self.e5DeathThreshold,
                    e6ReproductionThreshold = self.e6ReproductionThreshold,
                )

    # If another adjacent tile would have provided greater utility this round, AND this agent is suffering, move to the best tile.
    def move(self):
        if (self.food[0] + self.food[1] > self.e5DeathThreshold and self.food[0] + self.food[1] < self.e6ReproductionThreshold):
            adjacentCells = self.cell.get_neighborhood(radius=1, include_center=True)
            cellPreference = self.cell
            score = self.food[0] + self.food[1]
            # print(self.model.grid._mesa_property_layers["IndividualAgYield"].data)
            # print(self.model.grid._mesa_property_layers["IndividualHGYield"].data)
            for cell in adjacentCells:
                newScore = cell.IndividualAgYield * self.preference[1] + cell.IndividualHGYield * self.preference[0]
                print(newScore)
                if newScore > score:
                    score = newScore
                    cellPreference = cell
            self.move_to(cellPreference)
        if self.age == 18 and self.random.randint(0,3) == 0:
            adjacentCells = self.cell.get_neighborhood(radius=1, include_center=True)
            choice = self.random.randint(0, len(adjacentCells))
            self.move_to(adjacentCells[choice])
