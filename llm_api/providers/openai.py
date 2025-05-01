from openai import OpenAI

client = OpenAI(api_key=api_key)
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key):

    def list_models(self):
        return client.models.list()["data"]

    def chat_completion(self, messages, model, stream=False):
        return client.chat.completions.create(model=model,
        messages=messages,
        stream=stream)
