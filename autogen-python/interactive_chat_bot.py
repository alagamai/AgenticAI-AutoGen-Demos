import streamlit as st

st.title("My Chat Demo")

# Chat history stored in session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input box
user_input = st.chat_input("Say something...")

if user_input:
    # Store user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate a bot reply (static demo)
    bot_reply = f"You said: {user_input}"

    # Store bot reply
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Display bot reply
    with st.chat_message("assistant"):
        st.write(bot_reply)
