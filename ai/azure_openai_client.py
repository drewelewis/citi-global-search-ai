import os
import openai
from app.config import config

class azure_openai_client:
    def __init__(self, api_version: str):
        
        # Check if the environment variables are set
        azure_endpoint = config.OPENAI_API_BASE
        if azure_endpoint is None:
            raise ValueError("Please set the environment variable '_OPENAI_API_BASE' to your Azure OpenAI endpoint.")

        azure_api_key = config.OPENAI_API_KEY
        if azure_api_key is None:
            raise ValueError("Please set the environment variable '_OPENAI_API_KEY' to your Azure OpenAI API key.")

        if api_version is None:
            raise ValueError("Please include the API version in the constructor.") 


        self.client = openai.AzureOpenAI(
                api_key=azure_api_key,  
                api_version=api_version,
                azure_endpoint=azure_endpoint
        )

    def completion(self, model: str, messages: list, response_object: object, max_tokens: int = 1000, temperature: float = 0.7):
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            logprobs=True,
            response_format=response_object
        )
        return response

    def embedding(self, input: str, model: str):
        response = self.client.embeddings.create(
            input=input,
            model=model
        )
        return response
