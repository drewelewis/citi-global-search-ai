import openai
from app.config import config

from pydantic import BaseModel

class ai_response(BaseModel):
    text: str
    errors: str

def completion(messages):
    
    # Check if the environment variables are set
    azure_endpoint = config.OPENAI_API_BASE
    if azure_endpoint is None:
        raise ValueError("Please set the environment variable '_OPENAI_API_BASE' to your Azure OpenAI endpoint.")

    azure_api_key = config.OPENAI_API_KEY
    if azure_api_key is None:
        raise ValueError("Please set the environment variable '_OPENAI_API_KEY' to your Azure OpenAI API key.")

    api_version = config.OPENAI_API_VERSION
    if api_version is None:
        raise ValueError("Please set the environment variable '_OPENAI_API_VERSION' to your Azure OpenAI API version.")

    model_deployment_name = config.OPENAI_API_MODEL_DEPLOYMENT_NAME
    if model_deployment_name is None:
        raise ValueError("Please set the environment variable '_OPENAI_API_MODEL_DEPLOYMENT_NAME' to your Azure OpenAI deployment name.")

    client = openai.AzureOpenAI(
            api_key=azure_api_key,  
            api_version=api_version,
            azure_endpoint=azure_endpoint
    )

    response = client.beta.chat.completions.parse(  
        model=model_deployment_name,  
        messages=messages,
        temperature=1,
        logprobs=True,
        response_format=ai_response
    )  
    return response

if __name__ == "__main__":
    pass