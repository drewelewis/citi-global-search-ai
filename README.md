# IntuitAI

Location for code required to demo Open AI

# Getting Started

* First set virtual environment running env_creeate.bat
* Activate the virtual envirnonment using env_activate.bat
* Then, at the root of your project, run pip install -r requirements.txt to install dependencies
* Ensure you have data to be indexed in the content directory, data will be generated by the /scapers scripts.
* Run Create Index  database/create_index.py  This will create your index in Redis that will be used to store your embeddings.
* Run Create Vectors database/insert_data.py  This script will connect to Azure OpenAI to get the vector embedding and will then store the result in your Redis Index.

* Once you have an index and have created your embeddings, you will interact with SearchIndex.py as the entry point.

#References

https://github.com/openai/openai-cookbook/tree/main/examples/vector_databases/redis


#Docker

A Dockerfile was used intially to run Redis, now just use docker compose at the root directory.

up.bat   //to bring Redis up

down.bat  // to bring Redis down

#Redis

Redis will run as a docker container and store your vector embeddings.  The default username is undefined.  The default password is password.

Your code will connect to Redis and OpenAI using Environment Variables

Ensure you have values set for the following for Redis

_REDIS_HOST
_REDIS_PORT
_REDIS_PASSWORD

For OPENAI ensure you have the following values set using Environment Variables

_OPENAI_API_KEY
_OPENAI_API_BASE

#Todos

* Token calculation
* Feed prompt recursively
* Flush prompt as it approaches token limit
* Better Error handling, defensive programming


