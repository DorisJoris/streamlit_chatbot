import streamlit as st
import replicate
import os
import yaml

from utils import clear_chat_history, generate_response


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

    max_length = st.sidebar.slider(
        label='max_length',
        min_value=32,
        max_value=128,
        value=120,
        step=8
    )

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    st.sidebar.write(f'Latest messages from: {st.session_state.messages[-1]["role"]}')

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
prompt = st.chat_input(
    placeholder="Your message...",
    disabled = chat_disabled
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(
                client=client,
                messages=st.session_state.messages,
                prompt_input=prompt,
                llm=llm,
                temperature=temperature,
                top_p=top_p,
                max_length=max_length
            )
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)