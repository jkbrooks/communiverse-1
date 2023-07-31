import os
from typing import Any

class LanguageModel:
    def __init__(self, chat_model: Any, model_name: str = "gpt-3.5-turbo", 
                 openai_api_key: str = os.environ.get("OPENAI_API_KEY")):

        self.language_model = chat_model(model_name= model_name, 
                              openai_api_key=openai_api_key, 
                              streaming=True)