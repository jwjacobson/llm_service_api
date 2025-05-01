from openai import OpenAI


from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def list_models(self):
        return self.client.models.list()["data"]

    def chat_completion(self, messages, model, stream=False):
        return self.client.chat.completions.create(model=model,
        messages=messages,
        stream=stream)
