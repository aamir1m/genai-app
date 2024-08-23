import requests
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import tiktoken

# Load environment variables from the .env file
load_dotenv()

deployment_name = "gpt-4o"
model_name = "gpt-4o"
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
version = "2024-02-01"

max_response_tokens = 300
token_limit = 4096

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

def num_tokens_from_messages(messages, model=model_name):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 3
    tokens_per_name = 1
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

while True:
    user_input = input("Q:")      
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1] 
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")
    print(conv_history_tokens)
    print(response.usage)

    


