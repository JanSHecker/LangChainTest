import os
from BuildingFactory import BuildingFactory
from ResourceFactory import ResourceFactory
from dotenv import load_dotenv
from entity_engine import EntityDetection
from story_engine import StoryEngine
from gamestate_engine import GameState, GameStateEngine
from gamestate import resources_catalog, buildings_catalog

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
    entity_detection = EntityDetection(api_key=GEMINI_API_KEY)
    resource_factory = ResourceFactory(api_key=GEMINI_API_KEY)
    building_factory = BuildingFactory(api_key=GEMINI_API_KEY)

    # Initial game state
    starting_resources = {
        "food": 20,
        "wood": 50,
        "stone": 30,
        "tools": 5
    }
    game_state = GameState(population=10, resources=starting_resources, buildings=[])

    intro(game_state)

    while True:
        user_input = input("\nYour action: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Thanks for playing!")
            break

        # Narration
        narration = story_engine.narrate(user_input, game_state)
        print(f"\nVillage Update: {narration}")


        # Entity extraction
        extracted_entities = entity_detection.extract_entities(
            narration,
            known_resources=resources_catalog.keys(),
            known_buildings=buildings_catalog.keys()
        )
        for resource in extracted_entities.new_resources:
            new_resource = resource_factory.create_resource(resource)
            resources_catalog[new_resource.name] = new_resource
        for building in extracted_entities.new_buildings:
            new_building = building_factory.create_building(building)
            buildings_catalog[new_building.name] = new_building

        # Game state update
        game_state = state_engine.update_state(narration, game_state)
        print(f"[DEBUG] Game State: {game_state.model_dump()}")


if __name__ == "__main__":
    main()