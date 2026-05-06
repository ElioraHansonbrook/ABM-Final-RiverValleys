from mesa import Agent
from model import RiverValley

class Person(Agent):
    def __init__(self, model: RiverValley, *args, **kwargs) -> None:
        super().__init__(model, *args, **kwargs)