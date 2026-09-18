import aisuite as ai

_MODEL = "ollama:qwen3"


def get_temperature(city: str) -> str:
    """Get the current temperature for a city

    Args:
      city: The name of the city

    Returns:
      The current temperature for the city
    """
    temperatures = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C",
    }
    return temperatures.get(city, "Unknown")


def ask(user_input: str) -> None:
    """Send a natural-language query to the LLM and print its response.

    Uses aisuite's automatic tool-calling loop: the client executes any tool
    calls the model requests and feeds the results back until the model
    produces its final answer (up to ``max_turns`` round-trips).

    Args:
        user_input: The natural-language question or instruction from the user.
    """
    client = ai.Client()
    messages = [{"role": "user", "content": user_input}]

    print("Thinking..")

    response = client.chat.completions.create(
        model=_MODEL,
        messages=messages,
        tools=[get_temperature],
        max_turns=2,
    )
    print(response.choices[0].message.content)


def main() -> None:
    while True:
        print("To exit, please press enter.")
        user_input: str = input("Enter a query: ")

        if not user_input or len(user_input) == 0:
            print("Exiting..")
            break

        ask(user_input)
