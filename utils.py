import streamlit as st


# Function to clear the chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLM response.
def gen_replicate_response(
        client,
        messages,
        prompt_input,
        llm,
        temperature,
        top_p
):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in messages:
        string_dialogue += dict_message["role"].capitalize()+ ":" + dict_message["content"] + "\n\n"
    output = client.run(
        llm, 
        input={
            "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
            "temperature":temperature,
            "top_p":top_p
        }
    )
    return output