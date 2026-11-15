
import streamlit as st
from google import genai
from document_assistant import show_document_assistant
from document_assistant import read_document

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


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


chat_message = st.chat_input(
    "Ask me anything...",
    accept_file="multiple",
    file_type=["pdf", "docx", "txt", "csv"]
)

prompt = None
uploaded_files = []

if chat_message:
    prompt = chat_message.text
    uploaded_files = chat_message.files


chat = st.chat_input(
    "Ask me anything...",
    accept_file="multiple",
    file_type=["pdf", "docx", "txt", "csv"]
)

prompt = chat.text if chat else None
uploaded_files = chat.files if chat else []

from document_assistant import read_document

if uploaded_files:
    document_text = ""

    for file in uploaded_files:
        try:
            text = read_document(file)
            document_text += f"\n\nDocument: {file.name}\n{text}"
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

    st.session_state["document_text"] = document_text[:60000]


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
                            "parts": [{"text": (
                                "Uploaded document:\n"
                                + st.session_state.get("document_text", "")
                                + "\n\nUser message:\n"
                                + m["content"]
                                if m["role"] == "user"
                                and st.session_state.get("document_text")
                                else m["content"]
                            )}]

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
