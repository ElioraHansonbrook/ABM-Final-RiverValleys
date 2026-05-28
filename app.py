"""
app.py

ABM Final Project - River Valley Model
© 2026 Eliora Hansonbrook
"""

from model import RiverValley
from mesa.visualization import Slider, SolaraViz, make_space_component
from mesa.visualization.components import PropertyLayerStyle, AgentPortrayalStyle

# Visualize the model
def propertyLayerVisualization_yields(layer):
    if layer.name == "IndividualHGYield":
        return PropertyLayerStyle(
            color = "red",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=50
        )
    
    if layer.name == "IndividualAgYield":
        return PropertyLayerStyle(
            color = "green",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=50
        )
    
def propertyLayerVisualization_methadology(layer):
    if layer.name == "FarmingProportion":
        return PropertyLayerStyle(
            color = "green",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=1
        )

def propertyLayerVisualization_infrastructure(layer):
    if layer.name == "Infrastructure":
        return PropertyLayerStyle(
            color = "gray",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=1
        )

def propertyLayerVisualization_basic(layer):
    if layer.name == "Fertility":
        return PropertyLayerStyle(
            color = "blue",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=10
        )

    if layer.name == "Population":
        return PropertyLayerStyle(
            color = "yellow",
            alpha=0.8,
            colorbar=True,
            vmin=0,
            vmax=5,
        )

def agent_portrayal(agent):
    return AgentPortrayalStyle(
        x = agent.cell.coordinate[1],
        y = agent.cell.coordinate[0],
        color = "red",
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
        label="Height",
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
        label="Farmed Portion per Person (e1)",
        value = 50,
        min = 1,
        max = 1000,
        step = 1,
    ),

    "e2FarmingDecayRate": Slider(
        label="Farming Decay Rate (e2)",
        value = 120,
        min = 1,
        max = 100,
        step = 1,
    ),

    "e3InfrastructureDecayRate": Slider(
        label="Infrastructure Decay Rate (e3)",
        value = 2,
        min = 1,
        max = 100,
        step = 1,
    ),

    "e4ReproductionFraction": Slider(
        label="Reproduction Success Rate (e4)",
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
        value = 7,
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
    components = [make_space_component(propertylayer_portrayal=propertyLayerVisualization_basic, agent_portrayal=agent_portrayal),
                  make_space_component(propertylayer_portrayal=propertyLayerVisualization_yields, agent_portrayal=agent_portrayal),
                  make_space_component(propertylayer_portrayal=propertyLayerVisualization_methadology, agent_portrayal=agent_portrayal),
                  make_space_component(propertylayer_portrayal=propertyLayerVisualization_infrastructure, agent_portrayal=agent_portrayal)],
    model_params=model_params,
    name="River Valley Model",
)