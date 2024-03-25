import streamlit as st
import replicate
import os
import yaml
import json

from utils import clear_chat_history, gen_replicate_response


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

# Replicate Credentials
with st.sidebar:
    st.title('Chatbot credentials')
    if 'REPLICATE_KEY' in st.secrets:
        st.success('API keys provided by streamlit!', icon='✅')
        REPLICATE_KEY = st.secrets['REPLICATE_KEY']
        os.environ['REPLICATE_API_TOKEN'] = REPLICATE_KEY
        chat_disabled = False
    else:
        st.warning('API keys missing!', icon='⚠️')
        chat_disabled = True

    client = replicate.Client(
        api_token=REPLICATE_KEY
    )

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox(
        label='Choose a model',
        options=models.keys(),
        key='selected_model'
    )

    llm = models[selected_model]

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

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    messages_len = 0
    for message in st.session_state.messages:
        messages_len += len(message['content'])
    st.sidebar.write(f'The length of all messages is now {messages_len} characters.')


chat_tab, stats_tab = st.tabs(["Chat", "Stats"])

# Display or clear chat messages
for message in st.session_state.messages:
    with chat_tab.chat_message(message["role"]):
        chat_tab.write(message["content"])

# User-provided prompt
prompt = st.chat_input(
    placeholder="Your message...",
    disabled = chat_disabled
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_tab.chat_message("user").write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with chat_tab.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = gen_replicate_response(
                client=client,
                messages=st.session_state.messages,
                prompt_input=prompt,
                llm=llm,
                temperature=temperature,
                top_p=top_p
            )
            placeholder = chat_tab.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
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