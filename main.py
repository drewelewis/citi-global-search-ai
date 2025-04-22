import redis
import openai
import os
import glob
import numpy as np
import time
import database.redis.search as search
import app.config as config
import ai.chat_completion as chat_completion

import database.redis.data_operations as data_operations

messages = []

system_message = """
You are a friendly AI assistant.
""".strip()

messages.append({"role": "system", "content": system_message})

def init_redis_data():
    data_operations.insert_data()
 
def main() -> None:
    init_redis_data()


    if len(messages)<3:
        print("\n How can I help you? \n")
         
    query= input("> ")
    
    messages.append({"role": "user", "content": query})

    completion = chat_completion.completion(messages)
    message=completion.choices[0].message.parsed
    if message:
        print(f"\n{message.text}\n")

        messages.append({"role": "assistant", "content": message.text})
    
    main()


if __name__ == "__main__":
    main()