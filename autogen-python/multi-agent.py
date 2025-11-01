import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    # Create model client (DeepSeek for text-based reasoning)
    ollama_client = OllamaChatCompletionClient(model="deepseek-coder:6.7b")

    # Define agents
    teacher = AssistantAgent(
        name="Teacher",
        model_client=ollama_client,
        system_message="You are a kind and clear math teacher. Explain concepts very simply and guide the student."
    )

    student1 = AssistantAgent(
        name="Student1",
        model_client=ollama_client,
        system_message="You are a curious math student who asks follow-up questions to understand the concept deeply."
    )

    student2 = AssistantAgent(
        name="Student2",
        model_client=ollama_client,
        system_message="You are a dummy math student who asks ir-relevant questions."
    )

    # Group chat with round-robin flow
    chat = RoundRobinGroupChat(
        participants=[teacher, student1, student2],
        termination_condition=MaxMessageTermination(max_messages=6),
    )

    # Start chat
    await Console(chat.run_stream(task="Can you explain how to solve 2 x 3?"))

    # Cleanly close client
    await ollama_client.close()


if __name__ == "__main__":
    asyncio.run(main())
