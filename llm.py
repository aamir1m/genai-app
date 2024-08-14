import requests
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

deployment_name = "gpt-4o"
api_key = os.getenv("AZURE_OPENAI_API_KEY")

version = "2024-02-01"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

client = AzureOpenAI(
  api_key = api_key,  
  api_version = version,
  azure_endpoint = endpoint
)

system_content = """
Assistant is a large language model trained by OpenAI. 
Instructions: 
-only answer questions related to microsoft. 
-If you're unsure of an answer or its not relevant say I'm dumb
Context:
- User is thinking about azure open ai service
"""

conversation = [
        {"role": "system", 
         "content": system_content},
        ]

while True:
    user_input = input("Q: ")
    conversation.append({ "role": "user", "content": user_input })
    response = client.chat.completions.create(
        model = deployment_name,
        messages = conversation
    )
    
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")
    print(response.usage)

    


