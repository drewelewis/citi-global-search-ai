
import redis
from openai import AzureOpenAI
import os
import glob
import numpy as np
import time
import tiktoken
import ai.azure_openai_client as azure_openai_client

def create(text: str) -> str:
    client = azure_openai_client.client("2024-08-01-preview")
    response = client.embedding(input=text, model="text-embedding-ada-002")
    embedding = response.data

    time.sleep(3) # sleep to avoid rate limit with emedding API    
    return embedding

def vectorize(embedding:str) -> str:
    vector = embedding[0].embedding
    #print(vector)  
    # convert to numpy array and bytes
    vector = np.array(vector).astype(np.float32).tobytes()
    #print(vector) 
    return vector

def vectorize_ascii(embedding:str) -> str:
    vector = embedding[0].embedding
    return vector
        
def token_count(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens