
import streamlit as st

st.set_page_config(
    page_title="AI Agent Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Agent Chatbot")
st.caption("AI Engineering Portfolio Project")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me something...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    response = (
        "Hello! I'm your AI chatbot prototype. "
        "LLM integration is coming next."
    )

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
