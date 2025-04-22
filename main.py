import redis
import openai
import os
import glob
import numpy as np
import time
import databases.redis.search as search
import app.config as config
import ai.chat_completion as chat_completion

messages = []

system_message = """
You are a friendly AI assistant who will generate sql queries for the user.
""".strip()

messages.append({"role": "system", "content": system_message})
 
def main() -> None:
    
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