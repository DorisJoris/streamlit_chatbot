import streamlit as st


# Function to clear the chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLM response.
def generate_response(
        client,
        messages,
        prompt_input,
        llm,
        temperature,
        top_p,
        max_length
):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = client.run(
        llm, 
        input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
            "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1
        }
    )
    return output