import replicate
import yaml

from clients.base import client, response


with open('models.yml', 'r') as file:
    models = yaml.safe_load(file)['replicate']

class Replicate_Response(response):
    def __init__(self, selected_model, run_input, output):
        self._selected_model = selected_model
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
        return self._selected_model


class Replicate_Client(client):
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
            init_prompt: str,
            messages: dict,
            prompt_input: str,
            selected_model: str,
            temperature: float,
            top_p: float
    ) -> response:
        prompt = init_prompt + " "
        
        for message_dict in messages:
            prompt += message_dict["role"] + ": " + message_dict["content"] + "\n\n"

        prompt += f"User: {prompt_input}"

        run_input = {
            "prompt": f"{prompt} Assistant:",
            "temperature": temperature,
            "top_p": top_p
        }

        output = self.client.run(
            selected_model,
            input=run_input
        )
        
        return Replicate_Response(selected_model, run_input, output)