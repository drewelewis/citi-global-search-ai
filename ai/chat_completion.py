import openai
from app.config import config
from ai.azure_openai_client import azure_openai_client
from models.model import ai_response

def completion(messages):
    client = azure_openai_client(api_version="2024-08-01-preview")
    completion = client.completion("gpt-4o-2", messages, ai_response, max_tokens=1000, temperature=0.7)
    return completion

if __name__ == "__main__":
    pass