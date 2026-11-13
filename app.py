
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Agent Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Agent Chatbot")
st.caption("Powered by Google Gemini | AI Engineering Portfolio")

# Read API key securely from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {
                            "role": (
                                "model"
                                if m["role"] == "assistant"
                                else "user"
                            ),
                            "parts": [{"text": m["content"]}]
                        }
                        for m in st.session_state.messages
                    ]
                )

                answer = response.text or "No response generated."
                st.write(answer)

            except Exception:
                answer = "Unable to generate a response. Please try again."
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
