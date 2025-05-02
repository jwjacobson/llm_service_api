import google.generativeai as genai
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def list_models(self):
        models = genai.list_models()
        return [model.name for model in models if "generateContent" in model.supported_generation_methods]

    def chat_completion(self, messages, model, stream=False):
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        generative_model = genai.GenerativeModel(model_name=model)

        if stream:
            response = generative_model.generate_content(prompt, stream=True)
            return response
        else:
            response = generative_model.generate_content(prompt)
            return {"content": response.text}
