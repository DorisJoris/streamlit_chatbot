# Streamlit-Chatbot

This project is a simple streamlit-chatbot which enables the user to experiment with different LLMs. 
The project is primarly based on streamlits blog "[How to build a llama 2 chatbot](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)".

To us the chatbot a .streamlit/secrets.toml file has to be added, containing api-tokens for the different providers.

```
Replicate = "replicate_api_key"
Openai = "openai_api_key
```

The streamlit-application can be run locally with:

```
streamlit run home.py
```