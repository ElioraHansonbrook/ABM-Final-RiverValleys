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
                preference = (0.99, 0.01), # Food acquisition preference
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
        # Kill if too old
        if self.age >= self.lifeExpectancy:
            self.remove()
    
    # Update the preference of the model as the first step in a round.
    def updatePreference(self):
        # Only try to update when some food was gathered to prevent divide by zero errors
        if self.food[0] + self.food[1] != 0:
            # Standard update, as specified in description
            updatedPreference = ((self.preference[0] + (self.food[0]/(self.food[0] + self.food[1])))/2,
                             (self.preference[1] + (self.food[1]/(self.food[0] + self.food[1])))/2)
            self.preference = updatedPreference
        # Prevent the emergence of infinitessimal preferences
        if self.preference[0] > 0.99:
            self.preference = (0.99, 0.01)
        elif self.preference[1] > 0.99:
            self.preference = (0.01, 0.99)
    
    # Confirm the agent doesn't starve to death; Attempt reproduction, if requirements are met
    def reproduction(self):
        # Calculate total food
        totalFood = self.food[0] + self.food[1]
        # Children and seniors should die at a higher rate than adults; this "bonus" is responsible for that
        bonus = 3 if self.age < 18 or self.age > 45 else 0
        # Kill agents who didn't get enough food
        if totalFood < self.e5DeathThreshold + bonus:
            self.remove()
        # Reproduce if possible
        if totalFood > self.e6ReproductionThreshold:
            # Confirm age is right for reproduction
            if self.age >= 18 and self.age <= 45 and self.random.randint(0,self.e4ReproductionFraction) == 0:
                # Add agent with similar preferences
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
        # Move 50% of the time if not getting enough food OR if mostly hunter-gatherer
        if ((self.food[0] + self.food[1] > self.e5DeathThreshold and self.food[0] + self.food[1] < self.e6ReproductionThreshold) or self.preference[0] >= 0.5) and self.random.randint(0,2) == 0:
            adjacentCells = self.cell.get_neighborhood(radius=1, include_center=True)
            # A special variant of the accumulator pattern to find the cell of best fit
            cellPreference = self.cell
            score = self.food[0] + self.food[1]
            for cell in adjacentCells:
                newScore = cell.IndividualAgYield * self.preference[1] + cell.IndividualHGYield * self.preference[0]
                #print(newScore)
                if newScore > score:
                    score = newScore
                    cellPreference = cell
            # Move to the cell of best fit
            self.move_to(cellPreference)
