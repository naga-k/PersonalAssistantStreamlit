import openai
import json
import os
from dotenv import load_dotenv

import streamlit as st
st.write("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])

# Retrieve the API key from SecretManager
# secret_manager = SecretManager()
# openai.api_key = st.get_secret('OPENAI_API_KEY')

# Define the file path for storing chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history for a specific session
def load_chat_history(session_id, chat_history_dir):
    chat_history_file = os.path.join(chat_history_dir, f"{session_id}.json")
    if os.path.exists(chat_history_file):
        with open(chat_history_file, "r") as file:
            return json.load(file)
    return []

# Function to save chat history for a specific session
def save_chat_history(session_id, chat_history, chat_history_dir):
    chat_history_file = os.path.join(chat_history_dir, f"{session_id}.json")
    with open(chat_history_file, "w") as file:
        json.dump(chat_history, file)

# Function to get assistant response using streaming
def get_assistant_response(user_input):
    client = openai.OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        stream=True,
    )
    assistant_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            assistant_response += chunk.choices[0].delta.content
    return assistant_response
