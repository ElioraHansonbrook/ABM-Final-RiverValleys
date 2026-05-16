from mesa import Agent
from model import RiverValley

class Person(Agent):
    def __init__(self,
                model: RiverValley,
                preference = (0.999, 0.001), # Food acquisition preference
                age = 0,
                lifeExpectancy = 80,
                *args,
                **kwargs) -> None:
        super().__init__(model, *args, **kwargs)
        self.preference = preference
        self.age = age
        self.lifeExpectancy = lifeExpectancy
        self.food = (0,0)

    # Update the age of the agent, and kill if needed
    def ageUpdates(self):
        pass
    
    # Update the preference of the model as the first step in a round.
    def updatePreference(self):
        pass
    
    # Attempt reproduction, if requirements are met
    def reproduction(self):
        pass

    # If another adjacent tile would have provided greater utility this round, AND this agent is suffering, move to the best tile.
    def move(self):
        pass