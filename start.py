import redis
import openai
import os
import glob
import numpy as np
import time
import database.search as search

# OpenAI API key
openai.api_key = os.getenv('_OPENAI_API_KEY')
openai.api_base = os.getenv('_OPENAI_API_BASE')
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview" 

# Redis connection details
redis_host = os.getenv('_REDIS_HOST')
redis_port = os.getenv('_REDIS_PORT')
redis_password = os.getenv('_REDIS_PASSWORD')


def main() -> None:


    print("")
    query = input("How can I help you? \n")

    #query="How do I record credit card transactions?"
    search.search(query)
    main()


def debug() -> None:
    print("openai.api_key={value}".format(value = openai.api_key))
    print("openai.api_base={value}".format(value = openai.api_base))
    print("openai.api_type{value}".format(value = openai.api_type))
    print("openai.api_version={value}".format(value = openai.api_version))
    print("redis_host={value}".format(value = redis_host))
    print("redis_port={value}".format(value = redis_port))
    print("redis_password={value}".format(value = redis_password))

def debug2(string: str, encoding_name: str) -> None:
    pass

main()