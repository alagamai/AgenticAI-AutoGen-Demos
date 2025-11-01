import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image


async def main(task_type="code", task_input=None, image_path=None):
    if task_type == "code":
        ollama_client = OllamaChatCompletionClient(model="deepseek-coder:6.7b")
        assistant = AssistantAgent(name="assistant", model_client=ollama_client, model_client_stream=True)
        if not task_input:
            raise ValueError("Provide task_input for code/text tasks")
        await Console(assistant.run_stream(task=task_input))

    elif task_type == "vision":
        if not image_path:
            raise ValueError("Provide image_path for vision tasks")
        ollama_client = OllamaChatCompletionClient(model="llava:7b")
        assistant = AssistantAgent(name="assistant", model_client=ollama_client,
                                   #system_message="You give your observation in 5 lines.",
                                   )
        img = Image.from_file(image_path)

        multimodal_msg = MultiModalMessage(content=["What do you see in this image?", img], source="user")

        await Console(assistant.run_stream(task=multimodal_msg))
    else:
        raise ValueError("task_type must be either 'code' or 'vision'")

    await ollama_client.close()

# Example usage:
# asyncio.run(main(task_type="code", task_input="Write a Python function to reverse a string"))
asyncio.run(main(task_type="vision", image_path="image.jpg"))
