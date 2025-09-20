import os
from dotenv import load_dotenv
from story_engine import StoryEngine
from gamestate_engine import GameState, GameStateEngine

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Please set the GEMINI_API_KEY environment variable in your .env file.")
    exit(1)


def intro(game_state: GameState):
        import json
        print("""
==============================
    Medieval Village Manager
==============================
You are the leader of a small medieval village.
Your goal: help your people thrive by making wise decisions.

Type actions such as:
    - build a farm
    - send villagers to hunt
    - check resources
    - craft tools
    - construct buildings

The game will remember everything you do and update the village state.
Type 'quit' or 'exit' to leave the game.

This is the initial state of your village:
{state_json}
""".format(state_json=json.dumps(game_state.dict())))


def main():
    # Initialize engines
    story_engine = StoryEngine(api_key=GEMINI_API_KEY)
    state_engine = GameStateEngine(api_key=GEMINI_API_KEY)

    # Initial game state
    game_state = GameState(population=10, wood=50, stone=30, food=20, tools=5, buildings=[])

    intro(game_state)

    while True:
        user_input = input("\nYour action: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Thanks for playing!")
            break

        # Narration
        narration = story_engine.narrate(user_input, game_state)
        print(f"\nVillage Update: {narration}")

        # Game state update
        game_state = state_engine.update_state(narration, game_state)
        print(f"[DEBUG] Game State: {game_state.dict()}")


if __name__ == "__main__":
    main()