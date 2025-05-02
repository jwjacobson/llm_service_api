from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def list_models(self):
        pass

    @abstractmethod
    def chat_completion(self, messages, model, stream=False):
        pass
