import redis
import openai
import os
import glob
import numpy as np
import time
import database.redis.search as search
import app.config as config
import ai.azure_openai_client as azure_openai_client
from models.model import ai_response

import database.redis.data_operations as data_operations

messages = []

system_message = """
You are a friendly AI assistant.
""".strip()

messages.append({"role": "system", "content": system_message})
 
def main() -> None:
    # data_operations.insert_data()


    if len(messages)<3:
        print("\n How can I help you? \n")
         
    query= input("> ")
    
    messages.append({"role": "user", "content": query})
    client = azure_openai_client.client("2024-08-01-preview")
    completion = client.completion("gpt-4o-2", messages, ai_response, max_tokens=1000, temperature=0.7)
    message=completion.choices[0].message.parsed

    if message:
        print(f"\n{message.text}\n")

        messages.append({"role": "assistant", "content": message.text})
    
    main()


if __name__ == "__main__":
    main()