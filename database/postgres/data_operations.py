import os
import sys

import openai
import glob
import numpy as np
import time
import json
from app.config import config

import psycopg2
from pgvector.psycopg2 import register_vector

import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens

# Redis connection details
postgres_connection_string = config.POSTGRES_CONNECTION_STRING

def enable_pgvector(): 
    # Connect to the Redis server
    conn = psycopg2.connect(postgres_connection_string)

    sql="""
       CREATE EXTENSION vector;  
    """.strip()
    execute_sql(sql)

def create_tables(): 
    # Connect to the Redis server
    conn = psycopg2.connect(postgres_connection_string)
    sql="""
       CREATE TABLE IF NOT EXISTS articles (  
            article_id uuid UNIQUE PRIMARY KEY DEFAULT gen_random_uuid(),  
            url VARCHAR(200) NOT NULL, 
            title VARCHAR(200) NOT NULL, 
            text TEXT  NOT NULL, 
            text_embedding vector(1536) NOT NULL, 
            text_token_count int NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """.strip()
    execute_sql(sql)

def execute_sql(sql: str, data: object = None) -> None: 
    conn = psycopg2.connect(postgres_connection_string)
    try:
        cur = conn.cursor()
        if data:
            cur.execute(sql, data)
        else:
            cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        # raise
    finally:
        cur.close()
        conn.close()

def insert_article(url, title, text, text_embedding, text_token_count) -> None: 
    conn = psycopg2.connect(postgres_connection_string)
    register_vector(conn)
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO articles (url, title, text, text_embedding, text_token_count) VALUES (%s, %s, %s, %s, %s)', (url, title, text, np.array(text_embedding), text_token_count))

        conn.commit()
    except Exception as e:
        print(e)
        # raise
    finally:
        cur.close()
        conn.close()

def search(query: str) -> None: 
    embedding= embeddings.create(query)
    embedding=embedding[0].embedding
    conn = psycopg2.connect(postgres_connection_string)
    register_vector(conn)
    try:
        cur = conn.cursor()        
        cur.execute('SELECT text FROM articles ORDER BY text_embedding <-> %s LIMIT 5', (np.array(embedding),))
        results = cur.fetchall() 
        print(results)
        conn.commit()
    except Exception as e:
        print(e)
        # raise
    finally:
        cur.close()
        conn.close()

def insert_data():
    # Create Index First, if not already created
    enable_pgvector()
    create_tables()
    content_folder = os.path.join(config.PROJECT_ROOT, 'content')
    files = content_folder+'\global_search\output\*.json'
    
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
            # for binary data only, redis uses binary, postres will use string
            # text_vector=embeddings.vectorize(embedding)

            insert_article(url, title, text, embedding[0].embedding, token_count)




#init()