# Medieval Village Game

This is a text-based game where you manage a small medieval village. The game uses LangChain to process your actions and maintain a strong memory of facts and game state.

## How to Play

- Run `main.py` to start the game.
- Enter actions such as "build a windmill" to manage your village
- The game will evaluate the sucess of your actions and remember facts and state as you play.

## Requirements

- Python 3.10+
- langchain
- openai

## Setup

1. Install dependencies:
   pip install langchain openai
2. Run the game:
   python main.py

## Notes

- You need an OpenAI API key set as the environment variable `OPENAI_API_KEY`.
