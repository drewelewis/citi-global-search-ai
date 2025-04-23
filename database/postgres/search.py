import numpy as np
from redis.commands.search.query import Query
import redis
from openai import AzureOpenAI
import os
from app.config import config

import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens
import database.redis.data_operations as redis_data_operations
import database.postgres.data_operations as postgres_data_operations

# Redis connection details
redis_host = config.REDIS_HOST
redis_port = config.REDIS_PORT
redis_password = config.REDIS_PASSWORD

def search(query: str, token_limit=2000) -> None:

    # Vectorize the query
    embedding= embeddings.create(query)
    token_count=embeddings.token_count(query,"gpt-4o")
    query_vector=embeddings.vectorize(embedding)
    results = postgres_data_operations.search(query)

    sources=[]
    total_tokens=0
    
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

    delimiter = '\n'
    single_str = delimiter.join(sources)
    cleandata=('\n---\n {0}'.format(single_str))

    return cleandata

def search_vectors(query_vector, client, top_k=5):
    
    base_query = "*=>[KNN 5 @text_embedding $vector AS vector_score]"
    query = Query(base_query).return_fields("url", "title", "text", "vector_score","text_token_count").sort_by("vector_score").dialect(2)    
 
    try:
        results = client.ft("articles").search(query, query_params={"vector": query_vector})
    except Exception as e:
        print("Error calling Redis search: ", e)
        return None
 
    return results
 
 


