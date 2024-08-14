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

response = client.chat.completions.create(
    model=deployment_name, 
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)