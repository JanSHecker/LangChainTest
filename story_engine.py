from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)


class StoryEngine:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model, api_key=api_key)

        self.system_prompt = (
            "You are the narrator of a medieval village management game. "
            "Narrate the consequences of the user's actions and describe the costs in resources without mentioning specific amounts. "
            "Evaluate the user input critically, if the action is unrealistic given the current game state, let the action succeed only partially or fail completely."
            "In your Evaluation focus on the available resources and the current state of the village and be strict when the user attempt to use resources that are not there."
            "take into account side effects: e.g reduced food because everyone is working on building a new structure"
            "Keep the story factual and don't embellish."
            "Use the provided summary of past actions and events to maintain continuity."
            "Use the provided game state to evaluate the outcome but do not restate a new game state or any specific resource amounts."
        )

        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm, max_token_limit=1000, return_messages=True
        )


        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template("{input}\n\nCurrent Game State: {game_state}")
        ])

    def narrate(self, user_input: str, game_state: dict) -> str:
        """Generate a narration for the user input, maintaining memory, with game state context."""
        chain_input = {
            "input": user_input,
            "history": self.memory.buffer,
            "game_state": game_state
        }
        messages = self.prompt.format_messages(**chain_input)
        response = self.llm.invoke(messages)
        text = response.content if hasattr(response, "content") else str(response)

        # Save context to memory
        self.memory.save_context({"input": user_input}, {"output": text})
        return text
