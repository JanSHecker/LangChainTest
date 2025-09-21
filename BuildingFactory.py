from openai import api_key
from gamestate import Building
#  BuildingFactory.py this file creates a new building using Gemini API via LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
class BuildingFactory:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
        model=model,
        api_key=api_key
)
        self.structured_llm = self.llm.with_structured_output(Building)
        self.system_prompt = (
            "You are a building creation engine for a medieval village management game. "
            "Your task is to create a new building based on a name. "
            "The building should conform to the Building schema. "
            "The values should be proportionate to the examples of other buildings provided" 
            "Output must be valid JSON matching the schema exactly."
        )
        self.prompt = f"{self.system_prompt}\nBuilding type: {{building_type}}\nCreate the building."
        
     
     

    def create_building(self, building_type: str) -> str:
        prompt = self.prompt.format(building_type=building_type)
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)