import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")


# ---------------- STREAMLIT UI -----------------
st.set_page_config(page_title="AI Interviewer", layout="wide")
st.title("🤖 AI Job Interview — AutoGen + Streamlit")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = None

if "model_client" not in st.session_state:
    st.session_state.model_client = None


def show_st_message(role, text):
    st.chat_message(role).write(text)
    st.session_state.messages.append((role, text))


# ---------------- AUTOGEN SETUP -----------------

async def setup_autogen(role):
    # Create a client for OpenRouter
    model_client = OpenAIChatCompletionClient(
        api_key=openrouter_api_key,
        model="openai/gpt-oss-20b:free",
        base_url="https://openrouter.ai/api/v1",
        model_info={
            "type": "chat",
            "vision": False,
            "function_calling": True,
            "structured_output": True,
            "json_output": False,
            "family": "openrouter",
            "context_length": 131072,
            "input_cost_per_token": 0,
            "output_cost_per_token": 0
        },
        extra_headers={"HTTP-Referer": "http://localhost"}

    )

    interviewer = AssistantAgent(
        name="Interviewer",
        model_client=model_client,
        system_message=(
            f"You are an HR interviewer conducting a job interview "
            f"for a {role} position. Ask ONE short question at a time. "
            f"Terminate when the candidate says STOP."
        )
    )

    candidate = UserProxyAgent(name="Candidate")

    career_coach = AssistantAgent(
        name="Career_Coach",
        model_client=model_client,
        system_message=(
            f"You are a career coach for {role} interviews. "
            f"Give VERY short (1-2 line) feedback after each answer."
        )
    )

    termination = TextMentionTermination("STOP")

    chat = RoundRobinGroupChat(
        participants=[interviewer, candidate, career_coach],
        termination_condition=termination,
    )

    st.session_state.model_client = model_client
    st.session_state.chat = chat


# ---------------- FIRST CHAT RUN -----------------

async def run_interview_once(role):
    await setup_autogen(role)

    show_st_message("system", f"Interview Started for role: **{role}** ✅")

    chat = st.session_state.chat

    async for event in chat.run_stream(
            task=f"conduct a job interview for a {role} position."):

        # ✅ CASE 1: event is dict
        if isinstance(event, dict):
            if event.get("type") == "message":
                sender = event.get("from", "Unknown")
                content = event.get("content", "")
                show_st_message(sender, content)

        # ✅ CASE 2: event is TextMessage object
        else:
            sender = getattr(event, "sender", getattr(event, "source", "Unknown"))
            content = getattr(event, "content", "")
            show_st_message(sender, content)


# ---------------- CONTINUE CHAT AFTER USER REPLY -----------------

async def continue_chat():
    chat = st.session_state.chat
    async for event in chat.run_stream():

        # ✅ dict event
        if isinstance(event, dict):
            if event.get("type") == "message":
                sender = event.get("from", "Unknown")
                content = event.get("content", "")
                show_st_message(sender, content)

        # ✅ TextMessage event
        else:
            sender = getattr(event, "sender", getattr(event, "source", "Unknown"))
            content = getattr(event, "content", "")
            show_st_message(sender, content)


# ---------------- STREAMLIT UI -----------------

job_role = st.text_input("Enter the Job Role (e.g., Data Scientist, Software Engineer):")

if st.button("✅ Start Interview"):
    if not job_role:
        st.error("Please enter a job role before starting the interview.")
    else:
        asyncio.run(run_interview_once(job_role))


candidate_msg = st.chat_input("Answer the latest interview question…")

if candidate_msg and st.session_state.chat:
    show_st_message("Candidate", candidate_msg)

    candidate_agent = st.session_state.chat.participants[1]
    candidate_agent.send(UserMessage(content=candidate_msg, source="user"))

    asyncio.run(continue_chat())
