import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# App title
st.title("🤖 Ask Anything AI")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box
user_input = st.chat_input("Type your question...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_input
    )

    answer = response.text

    # Show AI response
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})