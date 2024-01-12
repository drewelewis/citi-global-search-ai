
import redis
from openai import AzureOpenAI
import os
import glob
import numpy as np
import time
import tiktoken

def create(text: str) -> str:
    client = AzureOpenAI(
        api_key=os.getenv("_OPENAI_API_KEY"),  
        api_version="2023-12-01-preview",
        azure_endpoint = os.getenv("_OPENAI_API_BASE")
    )
    response = client.embeddings.create(
        input = text,
        model= "text-embedding-ada-002"
    )
    embedding = response.data

    time.sleep(5) # sleep for 1 second to avoid rate limit with emedding API    
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
    #print(vector)  
    # convert to numpy array and bytes
    #vector = np.array(vector).astype(np.float32)
    #print(vector) 
    return vector
        
def token_count(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens