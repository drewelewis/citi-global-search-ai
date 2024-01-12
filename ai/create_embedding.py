import os
from openai import AzureOpenAI


client = AzureOpenAI(
    api_key=os.getenv("_OPENAI_API_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint = os.getenv("_OPENAI_API_BASE")
    
)

response = client.embeddings.create(
    input = "Your text string goes here",
    model= "text-embedding-ada-002"
)


print(response.data)

