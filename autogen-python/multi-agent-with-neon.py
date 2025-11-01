import asyncio
from pathlib import Path

from autogen_agentchat.ui import Console
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools, McpWorkbench
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    server_params = StdioServerParams(
    command = "npx",
    args = [
        # "-y",
        "@neondatabase/mcp-server-neon",
        "start",
        "napi_cqghxfmslkp5xdo6v81vc5ihgp1cc5va82erk00dyxwmk9w93g79sq3ju9nxfy83",
    ],

    )
    # Discover all tools exposed by the MCP Filesystem server
    mcp_wb =  McpWorkbench(server_params)
    async with mcp_wb as mcp_tool:
        ollama_client = OllamaChatCompletionClient(model="mistral:instruct")

        # Create an AssistantAgent that can use the MCP tools
        agent = AssistantAgent(
            name="file_manager",
            model_client=ollama_client,
            workbench=mcp_tool,  # MCP tools for filesystem access
        )
        await Console(agent.run_stream(task="get latest record from neon db"))

        # # Example use: Creating a file via natural language
        # task_text = (
        #     "get output of ls command"
        # )
        # result = await agent.run(task=task_text, cancellation_token=CancellationToken())

        # print("Agent run result:", result)


if __name__ == "__main__":
    asyncio.run(main())
