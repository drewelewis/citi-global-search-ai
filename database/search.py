import numpy as np
from redis.commands.search.query import Query
import redis
from openai import AzureOpenAI
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens
 

# Redis connection details
redis_host = os.getenv('_REDIS_HOST')
redis_port = os.getenv('_REDIS_PORT')
redis_password = os.getenv('_REDIS_PASSWORD')


def search(query: str) -> None:
    token_limit=2000

    # Connect to the Redis server
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)
    
    if conn.ping():
        pass
        #print("Connected to Redis")
  
    # Vectorize the query
    embedding= embeddings.create(query)
    token_count=embeddings.token_count(query)
    query_vector=embeddings.vectorize(embedding)
    results = search_vectors(query_vector, conn)

    sources=[]
    total_tokens=0
    
    print ("")
    print ("OK, I found a few articles that explains this. Let me summarize what I found:")
    print ("")

    if results:
        for i, article in enumerate(results.docs):
            token_count=int(article.text_token_count)
            total_tokens = total_tokens+token_count
            if (total_tokens < token_limit):
                sources.append(article.text)

            score = 1 - float(article.vector_score)
            print(f"\t{i+1}. {article.url} (Score: {round(score ,3) }) (Tokens: {article.text_token_count })")

    else:
        print("No results found")
    
    #print("Total Tokens ={value}".format(value =total_tokens))

    #data =str.join(sources) 
    delimiter = '\n'
    single_str = delimiter.join(sources)
    cleandata=('\n---\n {0}'.format(single_str))

    client = AzureOpenAI(
    api_key=os.getenv("_OPENAI_API_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint = os.getenv("_OPENAI_API_BASE")
    
)
    
    response = client.chat.completions.create(
    model="gpt-35-turbo",
            messages=[
            { "role": "system", "content": "You are a friendly and polite assistant who has vast information on Citigroup.Your pourpose is to help customers find important information on the company." },
            { "role": "user", "content": "Based on the sources below, answer the following question: " + query +
                "\nHere is some data from a few sources:\n" + cleandata
                }
        ],
        temperature=0,
        max_tokens=1200
    )
    
    response_text=f"\n{response.choices[0].message.content}"
    print(response_text)


def search_vectors(query_vector, client, top_k=5):
    base_query = "*=>[KNN 5 @text_embedding $vector AS vector_score]"
    query = Query(base_query).return_fields("url", "title", "text", "vector_score","text_token_count").sort_by("vector_score").dialect(2)    
 
    try:
        results = client.ft("articles").search(query, query_params={"vector": query_vector})
    except Exception as e:
        print("Error calling Redis search: ", e)
        return None
 
    return results
 
 


