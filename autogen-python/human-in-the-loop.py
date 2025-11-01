import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    # Create model client (DeepSeek for text-based reasoning)
    ollama_client = OllamaChatCompletionClient(model="deepseek-coder:6.7b")

    problem_solver_msg = """
        "You are ProblemSolverAgent — an AI solving simple math problems. "
        "Respond in 1-2 lines ONLY. "
        "Show only your reasoning and the final answer. "
        "Do not write system instructions or summaries. "
        "Do not use extra explanations."
    """

    checker_msg = """
    "Respond as 'Looks correct' or 'Mistake found', nothing more."
        """

    human_supervisor_msg = """
    You are the Human Supervisor overseeing ProblemSolverAgent and CheckerAgent.
    You review their messages and approve or request corrections.
    Respond concisely with: APPROVE, REVISE, or ASK_CLARIFICATION.
    """

    # Define agents
    ProblemSolverAgent = AssistantAgent(
        name="ProblemSolverAgent",
        model_client=ollama_client,
        system_message= problem_solver_msg,
    )

    CheckerAgent = AssistantAgent(
        name="CheckerAgent",
        model_client=ollama_client,
        system_message=checker_msg,)

    humansupervisor = UserProxyAgent(
        name="human_supervisor")


    # Create the termination condition which will end the conversation when the user says "APPROVE".
    # termination = TextMentionTermination("APPROVE")
    termination = MaxMessageTermination(max_messages=6)

    # Group chat with round-robin flow
    chat = RoundRobinGroupChat(
        participants=[ProblemSolverAgent, CheckerAgent, humansupervisor],
        termination_condition=termination,
    )

    # Start chat
    await Console(chat.run_stream(
        task="Solve this problem in python: What is the sum of all even numbers from 1 to 20?"
    ))
    # Cleanly close client
    await ollama_client.close()


if __name__ == "__main__":
    asyncio.run(main())
