import replicate
import yaml

from clients.base import Client, Response


with open('models.yml', 'r') as file:
    models = yaml.safe_load(file)['replicate']


class ReplicateResponse(Response):
    def __init__(self, model, run_input, output):
        self._model = model
        self._run_input = run_input
        self._message = ''
        for item in output:
            self._message += item

    @property
    def message(self) -> str:
        return self._message

    @property
    def input(self) -> dict:
        return self._run_input

    @property
    def model(self) -> str:
        return self._model


class ReplicateClient(Client):
    def __init__(self, api_token):
        self._provider = "Replicate"
        self._models = models
        self.client = replicate.Client(
            api_token=api_token
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
        messages: dict,
        system_prompt: str,
        top_p: float,
        temperature: float
    ) -> Response:
        prompt = ""

        for message_dict in messages:
            prompt += message_dict["role"] + ": "
            prompt += message_dict["content"] + "\n\n"

        run_input = {
            "system_prompt": system_prompt,
            "prompt": f"{prompt} Assistant:",
            "temperature": temperature,
            "top_p": top_p
        }

        output = self.client.run(
            model,
            input=run_input
        )

        return ReplicateResponse(model, run_input, output)
