import asyncio
from pathlib import Path

from autogen_agentchat.ui import Console
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools, McpWorkbench
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():

    desktop = Path.home() / "PycharmProjects" / "AgenticAI"
    # Set up server parameters to start the MCP Filesystem server via npx
    # server_params = StdioServerParams(
    #     command="npx",
    #     args=["-y", "@modelcontextprotocol/server-filesystem",
    #           "/Users/alagammainagappan/Desktop"
    #           ]

    fs_server = StdioServerParams(
        command="npx",
        args=["@modelcontextprotocol/server-filesystem", "/Users/alagammainagappan/PycharmProjects/agstudio-demo/AI-Playwright-multi-agent"]
    )

    pw_server = StdioServerParams(
    command = "npx",
    args = [
        "@playwright/mcp@latest",
        "--headless",
    ],

    )
    # Discover all tools exposed by the MCP Filesystem server
    mcp_wb = McpWorkbench(fs_server, pw_server)

    async with mcp_wb as mcp_tool:
        ollama_client = OllamaChatCompletionClient(model="mistral:instruct")

        # Create an AssistantAgent that can use the MCP tools
        agent = AssistantAgent(
            name="playwright_builder",
            model_client=ollama_client,
            workbench=mcp_tool,  # MCP tools for filesystem access
        )
        await Console(agent.run_stream(task="create a playwright project under folder test-pw, write script to automate test to go to url https://alagamai.vercel.app/ and enter access code qa-alagamai and click login"))


if __name__ == "__main__":
    asyncio.run(main())
