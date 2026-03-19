import streamlit as st
from google import genai
import os

# --- 1. SECURE KEY HANDLING ---
# This check handles both local development and Streamlit Cloud
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key is missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# --- 2. APP UI ---
st.title("🤖 Ask Anything AI")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Type your question...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # Updated to the stable model name
            contents=user_input
        )
        answer = response.text

        # Show AI response
        with st.chat_message("assistant"):
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")