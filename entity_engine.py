from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json

class OutcomeEntities(BaseModel):
    known_resources: list[str] = Field(..., description="List of resources already known to the game engine")
    new_resources: list[str] = Field(..., description="List of resources newly discovered in the narration")
    known_buildings: list[str] = Field(..., description="List of buildings already known to the game engine")
    new_buildings: list[str] = Field(..., description="List of buildings newly discovered in the narration")

class EntityDetection:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key
        )
        self.structured_llm = self.llm.with_structured_output(OutcomeEntities)
        self.system_prompt = (
            "You are an entity extraction engine for a medieval village management game. "
            "Your task is to extract and categorize entities from the narration provided by the story engine. "
            "Entities to extract include resources (food, wood, stone, tools) and buildings (farm, quarry, lumber mill, blacksmith). "
            "Distinguish between entities already known to the game engine and new entities introduced in the narration. "
            "Output must be valid JSON matching the schema exactly."
        )
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(
                "Narration: {narration}\nKnown resources (JSON): {known_resources_json}\nKnown buildings (JSON): {known_buildings_json}\nExtract and categorize entities."
            )
        ])

    def extract_entities(self, narration: str, known_resources: list[str], known_buildings: list[str]) -> OutcomeEntities:
        """
        Extract and categorize entities from the narration.
        """
        chain_input = {
            "narration": narration,
            "known_resources_json": json.dumps(known_resources),
            "known_buildings_json": json.dumps(known_buildings)
        }
        messages = self.prompt.format_messages(**chain_input)
        extracted_entities = self.structured_llm.invoke(messages)
        return extracted_entities