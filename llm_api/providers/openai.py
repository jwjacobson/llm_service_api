import openai
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key):
        openai.api_key = api_key

    def list_models(self):
        return openai.Model.list()["data"]

    def chat_completion(self, messages, model, stream=False):
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=stream,
        )
