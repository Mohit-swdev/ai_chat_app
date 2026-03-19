import streamlit as st
from google import genai
import os

# --- SECURE KEY HANDLING ---
# Streamlit Cloud uses st.secrets; local uses environment variables
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key is missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize the modern Gemini client
client = genai.Client(api_key=api_key)

st.title("🚀 Gemini 3 AI Chat")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        # Using gemini-3-flash: The 2026 workhorse model
        # Changed to the 2026 stable preview ID
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        full_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        if "429" in str(e):
            st.error("⏳ Quota reached. Please wait a moment before the next request.")
        elif "404" in str(e):
            st.error("❌ Model not found. We might need to update the model name string.")
        else:
            st.error(f"⚠️ Error: {e}")