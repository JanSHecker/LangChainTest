# ResourceFactory.py this file creates a new resource using Gemini API via LangChain
from gamestate import Resource, resources_catalog
# ResourceFactory.py this file creates a new resource using Gemini API via LangChain
from langchain_google_genai import ChatGoogleGenerativeAI

class ResourceFactory:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key
        )
        self.structured_llm = self.llm.with_structured_output(Resource)
        self.system_prompt = (
            "You are a resource creation engine for a medieval village management game. "
            "Your task is to create a new resource based on a name. "
            "The resource should conform to the Resource schema. "
            "The values should be proportionate to the examples of other resources provided. "
            "Output must be valid JSON matching the schema exactly."
        )
        # Prepare context of existing resources
        resources_info = "\n".join([
            f"- {name}: gold_cost_per_unit={res.gold_cost_per_unit}"
            for name, res in resources_catalog.items()
        ])
        self.prompt = (
            f"{self.system_prompt}\n"
            f"Existing resources and their gold cost per unit:\n{resources_info}\n"
            "Resource type: {{resource_type}}\nCreate the resource."
        )

    def create_resource(self, resource_type: str) -> str:
        prompt = self.prompt.format(resource_type=resource_type)
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)