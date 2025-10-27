# AgenticAI – AutoGen & Ollama Setup in PyCharm

This project demonstrates using **AutoGen** and **Ollama** to run AI agents, including **DeepSeek** (code/text) and **LLaVA** (vision/multimodal) models.

---

## Prerequisites

1. **Mac OS**
2. **Homebrew** installed
3. **Python 3.13** (recommended for compatibility)
4. **PyCharm** IDE installed
5. **Ollama** installed ([https://ollama.com/](https://ollama.com/))
6. Active **OpenAI API key** (optional if using OpenAI models)

---

## Step 1: Install Python 3.13 via Homebrew

```bash
brew install python@3.13
brew link --force --overwrite python@3.13
python3 --version   # should show Python 3.13.x
```

> If multiple Python versions exist, ensure `3.13` is in your `PATH`:

```bash
echo 'export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
python3 --version
```

---

## Step 2: Set up PyCharm Project

1. Open PyCharm.
2. **Create a new project** or open your existing project folder.
3. **Configure Python Interpreter**:
   - Go to **PyCharm → Preferences → Project: AgenticAI → Python Interpreter**
   - Click the gear → **Add** → select **Existing environment**
   - Browse to `/Users/<username>/PycharmProjects/AgenticAI/.venv/bin/python` (your venv)

---

## Step 3: Create Virtual Environment

In PyCharm terminal:

```bash
cd ~/PycharmProjects/AgenticAI
python3 -m venv .venv
source .venv/bin/activate
```

> Ensure the PyCharm interpreter points to this `.venv`.

---

## Step 4: Install Dependencies

```bash
python3 -m pip install --upgrade pip

# Install AutoGen and extensions
python3 -m pip install pyautogen autogen-ext openai ollama
```

---

## Step 5: Configure API Keys

- **OpenAI API Key** (if using OpenAI models):

```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxx"
```

- Add it in PyCharm:
  - Go to **Run → Edit Configurations → Environment Variables → Add OPENAI_API_KEY**
  - Paste your key.

---

## Step 6: Install and Run Ollama

1. Pull the models:

```bash
# Code/Text model
ollama pull deepseek-coder:6.7b

# Vision/Multimodal model
ollama pull llava:7b
```

2. Run Ollama server:

```bash
ollama serve
```

> Keep the Ollama server running while using your Python script.

---

## Step 7: Example Python Code – Multimodal Agent

`multimodal_agent.py`:

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image
from autogen_core.tools import ImageResultContent

async def main(task_type="code", task_input=None, image_path=None):
    """
    task_type: "code" for DeepSeek, "vision" for LLaVA
    task_input: string prompt for code/text
    image_path: local path to image if task_type="vision"
    """

    if task_type == "code":
        ollama_client = OllamaChatCompletionClient(model="deepseek-coder:6.7b")
        assistant = AssistantAgent(name="assistant", model_client=ollama_client)
        if not task_input:
            raise ValueError("Provide task_input for code/text tasks")
        await Console(assistant.run_stream(task=task_input))

    elif task_type == "vision":
        if not image_path:
            raise ValueError("Provide image_path for vision tasks")

        ollama_client = OllamaChatCompletionClient(model="llava:7b")
        assistant = AssistantAgent(name="assistant", model_client=ollama_client)

        # Convert image path to Image instance
        img = Image.from_file(image_path)

        # Wrap image in ImageResultContent
        image_msg = ImageResultContent(
            content="Here is the image I want you to analyze:",
            image=img
        )

        # Multi-modal message combining text and image
        multimodal_msg = MultiModalMessage(
            content=[
                "What do you see in this image?",
                image_msg
            ]
        )

        await Console(assistant.run_stream(task=multimodal_msg))

    else:
        raise ValueError("task_type must be either 'code' or 'vision'")

    await ollama_client.close()

# Example usage:
# For code/text tasks:
# asyncio.run(main(task_type="code", task_input="Write a Python function to reverse a string"))

# For vision/image tasks:
asyncio.run(main(task_type="vision", image_path="/Users/<username>/PycharmProjects/AgenticAI/image.jpg"))
```

---

## Step 8: Run in PyCharm

1. Open `multimodal_agent.py`.
2. Click **Run → Run 'multimodal_agent'**.
3. Terminal should show the AI agent responding for **code** or **vision** tasks.

---

## Notes

- Ensure **Ollama server is running** before executing scripts.
- Use Python 3.13 for compatibility.
- Use `task_type="code"` for DeepSeek and `"vision"` for LLaVA.
- For OpenAI, monitor your **API usage** to avoid rate-limit errors.

