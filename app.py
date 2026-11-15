
import streamlit as st
from google import genai
from document_assistant import show_document_assistant

st.set_page_config(
    page_title="AI Agent Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Agent Chatbot")
st.caption("Welcome to Hareesh Portfolio ChatBot")

# Read API key securely from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

# PDF & Document Assistant
if st.sidebar.button("📄 Document Assistant"):
    st.session_state["show_documents"] = True

if st.session_state.get("show_documents", False):
    if st.sidebar.button("⬅️ Back to Chatbot"):
        st.session_state["show_documents"] = False
        st.rerun()

    show_document_assistant(api_key)
    st.stop()


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
                    model="gemini-3-flash-preview",
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
                
                
            except Exception as e:
                answer = "Unable to generate a response."
                st.error(answer)
                st.error(f"Gemini API details: {str(e)}")
                
                status = getattr(e, "code", None)
                print(
                    f"Gemini HTTP status: {status}",
                    flush=True
                )


    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
