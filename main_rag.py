import ai.azure_openai_client as azure_openai_client
from models.model import ai_response

import database.redis.search as redis_search
import database.postgres.search as postgres_search

import database.redis.data_operations as redis_data_operations
import database.postgres.data_operations as postgres_data_operations
messages = []

system_message = """
You are a friendly and polite assistant who has vast information on Citigroup. Your purpose is to help customers find important information on the company. Only use information that you find from the documents that are given.  If you can't find relevant information, just say so.
""".strip()

messages.append({"role": "system", "content": system_message})
 
def main() -> None:
    # Seed the vector databases
    # redis_data_operations.insert_data()
    # postgres_data_operations.insert_data()
    
    if len(messages)<3:
        print("\n How can I help you? \n")
         
    query= input("> ")
    
    search_results = postgres_search.search(query, token_limit=2000)
    messages.append({"role": "user", "content": "Based on the sources below, answer the following question: " + query + "\nHere is some data from a few sources:\n" + search_results})

    client = azure_openai_client.client("2024-08-01-preview")
    completion = client.completion("gpt-4o-2", messages, ai_response, max_tokens=1000, temperature=0.7)
    message=completion.choices[0].message.parsed

    if message:
        print(f"\n{message.text}\n")
        messages.append({"role": "assistant", "content": message.text})
    
    main()

if __name__ == "__main__":
    main()