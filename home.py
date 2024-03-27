import streamlit as st
import yaml
import json

from utils import clear_chat_history, save_session_state
from clients import clients_dict


# Prepare session_state
if "saves" not in st.session_state.keys():
    with open('saves.yml', 'r') as file:
        st.session_state.saves = yaml.safe_load(file)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "How may I assist you today?"
        }
    ]

if "system_prompts" not in st.session_state.keys():
    with open('system_prompts.yml', 'r') as file:
        st.session_state.system_prompts = yaml.safe_load(file)

if "selected_system_prompt" not in st.session_state.keys():
    st.session_state.selected_system_prompt = list(
        st.session_state.system_prompts.keys()
    )[0]

if "system_prompt" not in st.session_state.keys():
    st.session_state.system_prompt = st.session_state.system_prompts[
        st.session_state.selected_system_prompt
    ]

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


stats_tab.subheader('Statistics')
n_messages = len(st.session_state.messages)
total_len_messages = 0
tokens = []
for message in st.session_state.messages:
    total_len_messages += len(message['content'])
    tokens = tokens + message['content'].split()
average_len_messages = total_len_messages/n_messages
stats_tab.write(f'{n_messages} included in the chat,')
stats_tab.write(f'with a total length of {total_len_messages}')
stats_tab.write(f'and a average length of {average_len_messages}.')
stats_tab.write(f'There are a total of {len(tokens)} words in the chat.')

stats_tab.subheader('Messages-dict')
stats_tab.json(json.dumps(st.session_state.messages, indent=2))
