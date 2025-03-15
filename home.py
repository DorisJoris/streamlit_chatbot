import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import pprint

from utils import clear_chat_history, save_session_state, load_save
from clients import clients_dict


# Prepare session_state
if "saves" not in st.session_state.keys():
    with open('saves/init_save.yml', 'r') as file:
        st.session_state.saves = yaml.safe_load(file)

    with open('saves/saves.yml', 'r') as file:
        saves = yaml.safe_load(file)
        if saves:
            st.session_state.saves.update(saves)

    st.session_state = load_save('init', st.session_state)

# App title
st.set_page_config(page_title="Joris LLM Chatbot")

st.session_state.saves = save_session_state('autosave', st.session_state)

# Sidebar
with st.sidebar:
    popcol1, popcol2 = st.columns(2)
    with popcol1.popover('Provider and Model'):
        selected_provider = st.selectbox(
            label='Choose a LLM provider',
            options=clients_dict.keys(),
            key='selected_provider'
        )

        client = clients_dict[selected_provider](
            api_token=st.secrets[selected_provider]
        )

        selected_model_name = st.selectbox(
            label='Choose a model',
            options=client.models.keys(),
            key='selected_model'
        )

        selected_model = client.models[selected_model_name]

    with popcol2.popover('Parameter'):
        temperature = st.slider(
            label='Temperature',
            min_value=0.01,
            max_value=2.0,
            value=1.0,
            step=0.01
        )

        top_p = st.slider(
            label='top_p',
            min_value=0.01,
            max_value=1.0,
            value=0.9,
            step=0.01
        )
    with st.container():
        st.subheader("System prompt")
        st.session_state.selected_system_prompt = st.selectbox(
            label="Select a system prompt",
            options=st.session_state.system_prompts.keys(),
            index=list(st.session_state.system_prompts.keys()).index(
                st.session_state.selected_system_prompt
            )
        )
        st.session_state.system_prompt = st.text_area(
            label="System prompt to the LLM.",
            value=st.session_state.system_prompts[
                st.session_state.selected_system_prompt
            ],
            height=400
        )
        if st.session_state.system_prompt not in st.session_state.system_prompts.values():
            next_user_nr = sum(
                1 for i in st.session_state.system_prompts.keys() if "User " in i
            ) + 1

            savecol1, savecol2 = st.columns(2)
            new_sp_name = savecol1.text_input(
                label="Name of your new system prompt",
                value=f"User {next_user_nr}"
            )
            savecol2.write("")
            savecol2.write("")
            if savecol2.button("Save system prompt"):
                st.session_state.system_prompts[new_sp_name] = st.session_state.system_prompt
                st.session_state.selected_system_prompt = new_sp_name
                st.rerun()


# Main area
chat_tab, stats_tab = st.tabs(["Chat", "Stats"])

chat_tab.button('Clear Chat History', on_click=clear_chat_history)

chat_messages_container = chat_tab.container(height=500, border=True)
# Display or clear chat messages
for message in st.session_state.messages:
    chat_messages_container.chat_message(
        message["role"]
    ).write(message["content"])

# User-provided prompt
prompt = chat_tab.chat_input(
    placeholder="Your message...",
    disabled=False
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_messages_container.chat_message("user").write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with chat_messages_container.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.generate_response(
                model=selected_model,
                messages=st.session_state.messages,
                system_prompt=st.session_state.system_prompt,
                top_p=top_p,
                temperature=temperature
            )
            st.markdown(response.message)
    message = {"role": "assistant", "content": response.message}
    st.session_state.messages.append(message)


stats_tab.subheader('Saves')

stats_tab.text(pprint.pformat(st.session_state.saves))
