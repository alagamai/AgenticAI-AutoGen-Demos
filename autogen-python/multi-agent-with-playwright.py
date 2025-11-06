import asyncio
import os
import subprocess

from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.ui import Console


async def main():
    # ✅ 1. Ensure the test folder exists
    folder_path = "/Users/alagammainagappan/PycharmProjects/AgenticAI/autogen-python/test-folder"
    os.makedirs(folder_path, exist_ok=True)

    # ✅ 2. Ensure Playwright is installed (optional but helpful)
    # try:
    #     subprocess.run(["npx", "playwright", "--version"], check=True)
    # except subprocess.CalledProcessError:
    #     print("Installing Playwright...")
    #     subprocess.run(["npx", "playwright", "install", "--with-deps"], check=True)

    # 3️⃣ Define MCP servers with explicit runtime for Mac compatibility
    fs_params = StdioServerParams(
        command="npx",
        args=["@modelcontextprotocol/server-filesystem", folder_path],
        runtime="node"
    )

    pw_params = StdioServerParams(
        command="npx",
        args=["-y", "@executeautomation/playwright-mcp-server"],
        runtime="node"
    )

    # 4️⃣ Choose a local Ollama model
    ollama_client = OllamaChatCompletionClient(model="llama3.1:latest")

    # 5️⃣ Create MCP workbenches and initialize them explicitly
    async with McpWorkbench(fs_params) as fs_wb, McpWorkbench(pw_params) as pw_wb:
        await fs_wb.initialize()
        await pw_wb.initialize()

        fs_agent = AssistantAgent(
            "filesystem_agent",
            model_client=ollama_client,
            workbench=fs_wb,
            model_client_stream=False  # disable streaming for clearer logs
        )

        pw_agent = AssistantAgent(
            "playwright_agent",
            model_client=ollama_client,
            workbench=pw_wb,
            model_client_stream=False  # disable streaming for clearer logs
        )

        # 6️⃣ Create team & run multi-agent workflow with relative path prompt
        team = RoundRobinGroupChat(
            [fs_agent, pw_agent],
            termination_condition=TextMessageTermination(source="playwright_agent")
        )

        await Console(
            team.run_stream(
                task="Create a new Playwright project in the current directory and verify installation."
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
