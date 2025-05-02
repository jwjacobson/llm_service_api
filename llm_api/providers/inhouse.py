from openai import OpenAI

from .base import LLMProvider

class InhouseProvider(LLMProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key, base_url="https://model-service.internal")

    def list_models(self):
        return [model.id for model in self.client.models.list()]

    def chat_completion(self, messages, model, stream=False):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
