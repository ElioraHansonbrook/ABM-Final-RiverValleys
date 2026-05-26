"""
app.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from model import RiverValley
from mesa.visualization import Slider, SolaraViz, make_space_component
from mesa.visualization.components import PropertyLayerStyle

# Visualize the model
def propertyLayerVisualization(layer):
    return PropertyLayerStyle(
        color = "blue",
        alpha=0.8,
        colorbar=True,
        vmin=0,
        vmax=10
    )

# Visual parameters to control the model
model_params = {
    "seed": Slider(
        label="Random Seed",
        value = 31415926535,
        min = 0,
        max = 9223372036854775807, # Largest signed 64-bit integer
        step = 1,
    ),
    "width": Slider(
        label="Width",
        value = 10,
        min = 5,
        max = 50,
        step = 1,
    ),
    "height": Slider(
        label="Width",
        value = 10,
        min = 5,
        max = 50,
        step = 1,
    ),

    "agentCount": Slider(
        label="Initial Population Count",
        value = 25,
        min = 10,
        max = 100,
        step = 1,
    ),

    "e1FarmedPortionPerPerson": Slider(
        label="Farmed Thousandth of a Tile Per Person (e1)",
        value = 50,
        min = 1,
        max = 1000,
        step = 1,
    ),

    "e2FarmingDecayRate": Slider(
        label="Farming Decay Rate Percentage (e2)",
        value = 10,
        min = 1,
        max = 100,
        step = 1,
    ),

    "e3InfrastructureDecayRate": Slider(
        label="Infrastructure Decay Rate Percentage (e3)",
        value = 10,
        min = 0,
        max = 100,
        step = 1,
    ),

    "e4ReproductionFraction": Slider(
        label="Reproduction Success Rate Percentage (e4)",
        value = 10,
        min = 0,
        max = 100,
        step = 1,
    ),

    "e5DeathThreshold": Slider(
        label="Starvation Threshold (e5)",
        value = 5,
        min = 1,
        max = 100,
        step = 1,
    ),

    "e6ReproductionThreshold": Slider(
        label="Reproduction Threshold (e6)",
        value = 15,
        min = 1,
        max = 100,
        step = 1,
    ),

    "e7RiverFertilityValue": Slider(
        label="River Fertility Value (e7)",
        value = 1,
        min = 1,
        max = 10,
        step = 1,
    ),

    "c1InitialClimateLowerThreshold": Slider(
        label="Initial Climate Lower Threshold (c1)",
        value = 30,
        min = 5,
        max = 50,
        step = 1,
    ),

    "c2InitialClimateUpperThreshold": Slider(
        label="Initial Climate Upper Threshold (c2)",
        value = 34,
        min = 5,
        max = 50,
        step = 1,
    ),

    "c3DisruptionClimateLowerThreshold": Slider(
        label="Disruption Climate Lower Threshold (c3)",
        value = 14,
        min = 5,
        max = 50,
        step = 1,
    ),

    "c4DisruptionClimateUpperThreshold": Slider(
        label="Disruption Climate Upper Threshold (c4)",
        value = 24,
        min = 5,
        max = 50,
        step = 1,
    ),
}

model = RiverValley()

page = SolaraViz(
    model,
    components = [make_space_component(propertylayer_portrayal=propertyLayerVisualization)],
    model_params=model_params,
    name="River Valley Model",
)