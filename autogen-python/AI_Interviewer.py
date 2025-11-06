from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import UserMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
import asyncio

from dotenv import load_dotenv

import os

load_dotenv()
key = os.getenv("")


# Define your async main function
async def main():
    ollama_client = OllamaChatCompletionClient(model="llama3.2:1b", base_url="http://localhost:11434")  # async client

    result = await ollama_client.create(
        [UserMessage(content="Who was the first man on the moon?", source="user")])  # sync call
    # print(result)

    role = "Software Engineer"

    interviewer = AssistantAgent(
        name="Interviewer",
        model_client=ollama_client,
        system_message='''
            You are an HR interviewer conducting a job interview for a {role} position. "
            "Ask only one clear simple short question at a time and wait for the candidate's response before proceeding."
            "Terminate the interview if the candidate mentions 'STOP'.
        '''
    )

    candidate = UserProxyAgent(
        name="Candidate",
        description='''
        You are a job candidate applying for a {role} position.    
        Answer the interview questions thoughtfully and professionally.
        '''
        # input_func=input
        # input_func=Console.input_async
    )

    career_coach = AssistantAgent(
        name="Career_coach",
        model_client=ollama_client,
        system_message='''
         You are a career coach specializing in preparing candidates for {role} interviews.
         Provide feedback in ONLY 1–2 short lines.
        Be crisp, simple, and to the point.
        Do NOT give long explanations.
        Keep every message extremely short.      '''
    )

    # ✅ Termination condition

    termination = TextMentionTermination("STOP")
    # termination = UserProxyTextMentionTermination("STOP")

    # termination_condition = MaxMessageTermination(max_messages=10)

    chat = RoundRobinGroupChat(
        participants=[interviewer, candidate, career_coach],
        termination_condition=termination,
    )

    # ✅ Run the multi-agent chat
    await Console(chat.run_stream(task="conduct a job interview for a Software Engineer position."))

    await ollama_client.close()


# # ------------------- ENTRY POINT -------------------


# ✅ Proper async entrypoint
if __name__ == "__main__":
    asyncio.run(main())

