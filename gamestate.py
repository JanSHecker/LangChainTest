from pydantic import BaseModel, Field


class Resource(BaseModel):
    name: str = Field(..., description="Name of the resource")
    gold_cost_per_unit: int = Field(..., description="Gold cost per unit of the resource")

class Building(BaseModel):
    name: str = Field(..., description="Name of the building")
    construction_status: str = Field(..., description="Current construction status of the building")
    construction_costs: dict[str, int] = Field(..., description="Construction costs for the building")
    resource_production: dict[str, int] = Field(..., description="Resources produced by the building per time unit")

class GameState(BaseModel):
    population: int = Field(..., description="Number of villagers (cannot be negative)")
    resources: dict[str, int] = Field(..., description="Dictionary of resources and their quantities")
    buildings: list[Building] = Field(..., description="List of constructed buildings")


resources_catalog = {
    "food": Resource(name="food", gold_cost_per_unit=1),
    "wood": Resource(name="wood", gold_cost_per_unit=2),
    "stone": Resource(name="stone", gold_cost_per_unit=3),
    "tools": Resource(name="tools", gold_cost_per_unit=5),
}   
buildings_catalog = {
    "farm": Building(
        name="farm",
        construction_status="completed",
        construction_costs={"wood": 50, "stone": 30},
        resource_production={"food": 10}
    ),

    "quarry": Building(
        name="quarry",
        construction_status="completed",
        construction_costs={"wood": 40, "stone": 50},
        resource_production={"stone": 5}
    ),
    "lumber mill": Building(
        name="lumber mill",
        construction_status="completed",
        construction_costs={"wood": 30, "stone": 20},
        resource_production={"wood": 5}
    ),
    "blacksmith": Building(
        name="blacksmith",
        construction_status="completed",
        construction_costs={"wood": 20, "stone": 30, "iron": 10},
        resource_production={"tools": 5}
    ),
}