import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main() -> None:
    # Create a model client (ensure Ollama is running locally)
    model_client = OllamaChatCompletionClient(model="llama3.1:latest")

    # Math expert agent
    math_agent = AssistantAgent(
        name="math_expert",
        model_client=model_client,
        system_message="You are a math expert who can solve integrals and equations.",
        description="Expert in mathematics and symbolic computation.",
        model_client_stream=True,
    )
    math_tool = AgentTool(math_agent, return_value_as_last_message=True)

    # Chemistry expert agent
    chemistry_agent = AssistantAgent(
        name="chemistry_expert",
        model_client=model_client,
        system_message="You are a chemistry expert who knows molecular structures and calculations.",
        description="Expert in chemistry and molecular science.",
        model_client_stream=True,
    )
    chemistry_tool = AgentTool(chemistry_agent, return_value_as_last_message=True)

    # General assistant agent that can use the tools
    general_agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful general assistant. Use the math or chemistry tools when relevant.",
        model_client_stream=True,
        tools=[math_tool, chemistry_tool],
        max_tool_iterations=5,
    )

    # Run tasks through the console
    print("\n🧮 Running math task...")
    await Console(general_agent.run_stream(task="What is the integral of x^2?"))

    print("\n⚗️ Running chemistry task...")
    await Console(general_agent.run_stream(task="What is the molecular weight of water?"))


if __name__ == "__main__":
    asyncio.run(main())
