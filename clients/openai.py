from openai import OpenAI
import yaml

from clients.base import Client, Response


with open('models.yml', 'r') as file:
    models = yaml.safe_load(file)['openai-chat']


# --- A cliente and response class for the Openai chat.completion api ---
class OpenaiChatResponse(Response):
    def __init__(self, model, run_input, output):
        self._model = model
        self._run_input = run_input
        self._message = output.choices[0].message.content

    @property
    def message(self) -> str:
        return self._message

    @property
    def input(self) -> dict:
        return self._run_input

    @property
    def model(self) -> str:
        return self._model


class OpenaiChatClient(Client):
    def __init__(self, api_token):
        self._provider = "Openai"
        self._models = models
        self.client = OpenAI(
            api_key=api_token
        )

    @property
    def provider(self):
        return self._provider

    @property
    def models(self):
        return self._models

    def generate_response(
        self,
        model: str,
        messages: list,
        system_prompt: str,
        top_p: float,
        temperature: float
    ) -> Response:

        messages = [
            {"role": "system", "content": system_prompt}
        ] + messages

        run_input = {
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p
        }

        output = self.client.chat.completions.create(
            model=model,
            **run_input
        )

        return OpenaiChatResponse(model, run_input, output)
