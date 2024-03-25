from abc import ABC, abstractmethod

class response(ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        # Returns the generated respones message as a string.
        return self._message

class client(ABC):
    @property
    @abstractmethod
    def models(self) -> dict:
        # Returns a dictionary of aviable models,
        # with the key being a readable shortname and the value being the model ID.
        return self._models
    
    @abstractmethod
    def generate_response(self, *args, **kwargs) -> response:
        # returns a response object
        pass
