
import redis
import openai
import os
import glob
import numpy as np
import time
import tiktoken

# OpenAI API key
openai.api_key = os.getenv('_OPENAI_API_KEY')
openai.api_base = os.getenv('_OPENAI_API_BASE')
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the futur
    

def get_token_count(text: str, model: str, deployment_id: str) -> str:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    token_count = len(encoding.encode(text))
    return token_count