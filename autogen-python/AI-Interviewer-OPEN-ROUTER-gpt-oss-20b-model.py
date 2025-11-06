from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import UserMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
import asyncio

from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

import os

load_dotenv()
key = os.getenv("")


# Define your async main function
async def main():
    openrouter_api_key = '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'

    # Create a client for OpenRouter
    model_client = OpenAIChatCompletionClient(
        api_key=openrouter_api_key,
        model="openai/gpt-oss-20b:free",
        base_url="https://openrouter.ai/api/v1",
        model_info={
            "type": "chat",
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "context_length": 32768,
            "input_cost_per_token": 0,
            "output_cost_per_token": 0,
            "family": "openrouter",
            "structured_output": False

        },

        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Autogen Interview App"
        }

    )
    result = await model_client.create(
        [UserMessage(content="Who was the first man on the moon?", source="user")])  # sync call
    print(result)

    role = "Software Engineer"

    interviewer = AssistantAgent(
        name="Interviewer",
        model_client=model_client,
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
        model_client=model_client,
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

    await model_client.close()


# # ------------------- ENTRY POINT -------------------


# ✅ Proper async entrypoint
if __name__ == "__main__":
    asyncio.run(main())

