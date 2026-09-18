import requests
from typing import Any

from ollama import chat


def get_temperature(city: str) -> dict[str, str]:
    """Get the current temperature for a city

    Args:
      city: The name of the city

    Returns:
      The current temperature for the city
    """

    return {"New York": "15 Celcius", "London": "20 Celcius"}


def ask(user_input: str):
    """Send a natural-language query to the LLM and print its response.

    Runs a two-turn agentic loop using the qwen3 model via Ollama:
    1. Sends the user's message and waits for a response.
    2. If the model calls the ``get_temperature`` tool, executes it, appends
       the result to the conversation, and sends a second request so the model
       can incorporate the real data into its final answer.
    3. Prints the model's final content to stdout.

    Args:
        user_input: The natural-language question or instruction from the user.
    """
    messages: Any = [{"role": "user", "content": user_input}]

    print("Thinking..")

    # pass functions directly as tools in the tools list or as a JSON schema
    response = chat(
        model="qwen3", messages=messages, tools=[get_temperature], think=True
    )

    messages.append(response.message)
    if response.message.tool_calls:
        # only recommended for models which only return a single tool call
        call = response.message.tool_calls[0]
        result = get_temperature(**call.function.arguments)
        print("Running the toolchain..")
        # add the tool result to the messages
        messages.append(
            {
                "role": "tool",
                "tool_name": call.function.name,
                "content": str(result),
            }
        )

        final_response = chat(
            model="qwen3", messages=messages, tools=[get_temperature], think=True
        )
        print(final_response.message.content)


def main() -> None:

    while True:
        print("To exit, please press enter.")
        user_input: str = input("Enter a query: ")

        if not user_input or len(user_input) == 0:
            print("Exiting..")
            break

        ask(user_input)
