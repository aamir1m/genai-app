from flask import current_app as app
from openai import AzureOpenAI
import tiktoken

def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
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
    num_tokens += 3  # every reply is primed with assistant
    return num_tokens

def get_chat_response(user_input, conversation, model_name):
    """Generate a response from the LLM and update the conversation history."""
    api_key = app.config['AZURE_OPENAI_API_KEY']
    endpoint = app.config['AZURE_OPENAI_ENDPOINT']
    api_version = app.config['AZURE_OPENAI_API_VERSION']

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )

    conversation.append({"role": "user", "content": user_input})
    
    max_response_tokens = 300
    token_limit = 4096
    conv_history_tokens = num_tokens_from_messages(conversation, model=model_name)
    
    tokens_before_cut = conv_history_tokens
    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1]  # Remove the oldest user message
        conv_history_tokens = num_tokens_from_messages(conversation, model=model_name)

    response = client.chat.completions.create(
        model=model_name,
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens
    )

    response_message = response.choices[0].message.content
    
    tokens_current_response = len(tiktoken.encoding_for_model(model_name).encode(response_message))
    tokens_user_message = len(tiktoken.encoding_for_model(model_name).encode(user_input))
    
    return {
        "response": response_message,
        "conversation": conversation,
        "token_usage": {
            "user_message": tokens_user_message,
            "llm_response": tokens_current_response,
            "full_conversation": tokens_before_cut,
            "current_response": tokens_current_response
        }
    }