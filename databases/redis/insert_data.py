
import redis
import openai
import os
import sys
import glob
import numpy as np
import time
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
import databases.redis.utils as database_utils
import utilities.ai.embeddings as embeddings
import utilities.ai.tokens as tokens

# OpenAI API key
openai.api_key = os.getenv('_OPENAI_API_KEY')
openai.api_base = os.getenv('_OPENAI_API_BASE')
openai.api_type = os.getenv('_OPENAI_API_TYPE')
openai.api_version = os.getenv('_OPENAI_API_VERSION')

# Redis connection details
redis_host = os.getenv('_REDIS_HOST')
redis_port = os.getenv('_REDIS_PORT')
redis_password = os.getenv('_REDIS_PASSWORD')
    

def read_files():
    database_utils.create_index()
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
            token_count=embeddings.token_count(text)
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
read_files()