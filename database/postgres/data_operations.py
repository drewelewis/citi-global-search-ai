import os
import sys

import openai
import glob
import numpy as np
import time
import json
from app.config import config

import psycopg2

import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens

# Redis connection details
postgres_connection_string = config.POSTGRES_CONNECTION_STRING

    
def create_table(): 
    # Connect to the Redis server
    conn = psycopg2.connect(postgres_connection_string)
    sql="""
        CREATE TABLE articles (  
            article_id uuid UNIQUE PRIMARY KEY,  
            url VARCHAR(200) NOT NULL, 
            title VARCHAR(200) NOT NULL, 
            text TEXT  NOT NULL, 
            text_embedding embedding vector(1536) NOT NULL, 
            text_token_count int NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );  
    """.strip()
    
    # Create the index
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print("Table already exists")
    finally:
        cur.close()
        conn.close()


def insert_data():
    # Create Index First, if not already created
    create_index()
    content_folder = os.path.join(config.PROJECT_ROOT, 'content')
    files = content_folder+'\global_search\output\*.json'
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)
 
    p = conn.pipeline(transaction=False)
    for filepath in glob.glob(files):
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