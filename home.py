import streamlit as st
import yaml
import json

from utils import clear_chat_history
from clients import clients_dict



with open('models.yml', 'r') as file:
    models = yaml.safe_load(file)

# App title
st.set_page_config(page_title="Joris Llama 2 Chatbot")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "How may I assist you today?"
        }
    ]

# Sidebar
with st.sidebar:
    st.subheader('Models and parameters')
    
    selected_provider =st.sidebar.selectbox(
        label='Choose a LLM provider',
        options=clients_dict.keys(),
        key='selected_provider'
    )

    client = clients_dict[selected_provider](
        api_token=st.secrets[selected_provider]
    )

    selected_model_name = st.sidebar.selectbox(
        label='Choose a model',
        options=client.models.keys(),
        key='selected_model'
    )

    selected_model = client.models[selected_model_name]

    temperature = st.sidebar.slider(
        label='Temperature',
        min_value=0.01,
        max_value=5.0,
        value=0.1,
        step=0.01
    )

    top_p = st.sidebar.slider(
        label='top_p',
        min_value=0.01,
        max_value=1.0,
        value=0.9,
        step=0.01
    )

    init_prompt = st.sidebar.text_area(
        label="Initial prompt to the LLM.",
        value= ("You are a helpful assistant. "
                "You do not respond as 'User' or pretend to be 'User'. "
                "You only respond once as 'Assistant'.")
    )

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Main area
chat_tab, stats_tab = st.tabs(["Chat", "Stats"])

chat_messages_container = chat_tab.container()
# Display or clear chat messages
for message in st.session_state.messages:
    chat_messages_container.chat_message(
        message["role"]
    ).write(message["content"])

# User-provided prompt
prompt = chat_tab.chat_input(
    placeholder="Your message...",
    disabled = False
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_messages_container.chat_message("user").write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with chat_messages_container.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.generate_response(
                init_prompt=init_prompt,
                messages=st.session_state.messages,
                prompt_input=prompt,
                selected_model=selected_model,
                temperature=temperature,
                top_p=top_p
            )
            chat_messages_container.markdown(response.message)
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