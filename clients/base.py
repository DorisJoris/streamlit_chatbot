from abc import ABC, abstractmethod


class Response(ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        # Returns the generated respones message as a string.
        return self._message


class Client(ABC):
    @abstractmethod
    def __init__(self, api_key: str):
        pass

    @property
    @abstractmethod
    def models(self) -> dict:
        # Returns a dictionary of aviable models,
        # with the key being a readable shortname
        # and the value being the model ID.
        return self._models

    @abstractmethod
    def generate_response(
        self,
        model: str,
        messages: dict,
        system_prompt: str,
        top_p: float,
        temperature: float
    ) -> Response:
        # returns a response object
        pass
