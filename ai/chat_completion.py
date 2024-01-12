import os
from openai import AzureOpenAI


client = AzureOpenAI(
    api_key=os.getenv("_OPENAI_API_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint = os.getenv("_OPENAI_API_BASE")
    
)

response = client.chat.completions.create(
    model="gpt-35-turbo",
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "What's the difference between garbanzo beans and chickpeas?"}
    ],
)

#print(response)

response_message = response.choices[0].message.content

print(response_message)