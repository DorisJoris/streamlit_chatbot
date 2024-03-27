# Streamlit-Chatbot

This project is a simple streamlit-chatbot which enables the user to experiment with different LLMs. 
The project is primarly based on streamlits blog "[How to build a llama 2 chatbot](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)".

### API keys

To use the chatbot a .streamlit/secrets.toml file has to be added to the project-folder, containing api-tokens for the different providers.

```
Replicate = "replicate_api_key"
Openai-chat = "openai_api_key
```

You can create your own API-keys here:
- [OpenAI](https://openai.com/blog/openai-api)
- [Replicate](https://replicate.com/)


### Running the application locally
The streamlit-application can be run locally with:

```
streamlit run home.py
```