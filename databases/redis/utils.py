import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

import os
 
# Redis connection details
redis_host = os.getenv('_REDIS_HOST')
redis_port = os.getenv('_REDIS_PORT')
redis_password = os.getenv('_REDIS_PASSWORD')

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


