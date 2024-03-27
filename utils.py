import streamlit as st
from datetime import datetime
import yaml

# Function to clear the chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


def save_session_state(savename, session_state):
    session_state.saves[savename] = {}
    session_state.saves[savename]["time"] = datetime.now()
    for key, value in session_state.items():
        if key != "saves":
            session_state.saves[savename][key] = value

    with open('saves.yml', 'w') as file:
        yaml.dump(session_state.saves, file)

    return session_state.saves