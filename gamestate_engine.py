
# Unified imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json
from gamestate import GameState, buildings_catalog, resources_catalog



class GameStateEngine:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key
        )
        self.structured_llm = self.llm.with_structured_output(GameState)
        self.system_prompt = (
            "You are the authoritative game engine for a medieval village management game. "
            "Your task is to update the game state in response to the player's actions. "
            "Constraints: "
            "- Population, food, wood, stone, and tools cannot go below 0. "
            "- Buildings is a list of strings representing constructed buildings. "
            "- Do not narrate, do not include any extra text, only valid JSON. "
            "- Repeat current values if they do not change. "
            "- Update buildings list if buildings are constructed or destroyed. "
            "- If a building is unfinished, it should be added as '<current_state> <building_name>'"
            "- an action can reference an unfinished building and change its state. if it is completed remove the <state> prefix"
            "Always ensure JSON is valid and matches the schema exactly."
        )
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(
                "Available buildings and their details:\n{buildings_info}\n\n"
                "Available resources and their details:\n{resources_info}\n\n"
                "Player action: {user_input}\nCurrent game state (JSON): {game_state_json}\n"
                "Update the JSON to reflect the result of this action."
            )
        ])

    def update_state(self, user_input: str, current_state: GameState) -> GameState:
        """
        Update the structured game state given the user input.
        """
        # Prepare building information for the LLM
        buildings_info = ""
        for name, building in buildings_catalog.items():
            buildings_info += f"- {name}: Costs {building.construction_costs}, Produces {building.resource_production}\n"
        
        # Prepare resource information for the LLM
        resources_info = ""
        for name, resource in resources_catalog.items():
            resources_info += f"- {name}: Gold cost per unit = {resource.gold_cost_per_unit}\n"
        
        chain_input = {
            "user_input": user_input,
            "game_state_json": json.dumps(current_state.model_dump()),
            "buildings_info": buildings_info,
            "resources_info": resources_info
        }
        messages = self.prompt.format_messages(**chain_input)
        updated_state = self.structured_llm.invoke(messages)
        return updated_state