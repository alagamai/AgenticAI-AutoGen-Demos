from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
import asyncio

async def main():
    ollama_client = OllamaChatCompletionClient(
        model="deepseek-coder:6.7b",  # or any local Ollama model
        # You **do not** need base_url here, it auto-detects localhost:11434
    )

    assistant = AssistantAgent(
        name="assistant",
        model_client=ollama_client
    )

    await Console(assistant.run_stream(task="Write a Python function to reverse a string"))
    await ollama_client.close()

asyncio.run(main())
