import os
import sys
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.chdir('..')))
sys.path.append(PROJECT_ROOT)


import openai
import glob
import numpy as np
import time
import json
from app.config import config

import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens

# Redis connection details
redis_host = config.REDIS_HOST
redis_port = config.REDIS_PORT
redis_password = config.REDIS_PASSWORD
    
def create_index(): 
    # Connect to the Redis server
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)
    
    SCHEMA = [
        TextField("url"),
        TextField("text"),
        VectorField("text_embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"}),
    ]
    
    # Create the index
    try:
        conn.ft("articles").create_index(fields=SCHEMA, definition=IndexDefinition(prefix=["citi:"], index_type=IndexType.HASH))
    except Exception as e:
        print("Index already exists")

def insert_data():
    # Create Index First, if not already created
    create_index()

    folder_path = PROJECT_ROOT+'\content\global_search\output'
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)
 
    p = conn.pipeline(transaction=False)
    for filepath in glob.glob(os.path.join(folder_path, '*.json')):
        content_to_index=[]
        filename=os.path.basename(filepath).split('/')[-1]
        print(filename)
        
        with open(filepath, 'r', encoding="utf-8") as f:
            file_text = f.read()
            doc=json.loads(file_text)
            url=doc['url']
            title=doc['title']
            print(url)
            for tag in doc:
                if tag.count('tag-') > 0:
                    print (tag)
                    print (doc[tag])
                    content_to_index.append(doc[tag])
                    
            text = '\n'.join(content_to_index)
            #save file (text)
            
            embedding= embeddings.create(text)
            token_count=embeddings.token_count(text,"gpt-4o")
            text_vector=embeddings.vectorize(embedding)
            
            # Create a new hash with url and embedding
            article_hash = {
                "url": url,
                "title": title,
                "text": text,
                "text_embedding": text_vector,
                "text_token_count": token_count
            }
            # create hash
            conn.hset(name="citi:"+ filename, mapping=article_hash)
    #p.execute()


#init()