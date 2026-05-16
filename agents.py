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
    
    # Update the preference of the model as the first step in a round.
    def updatePreference(self):
        pass

    def collectFood(self):
        pass