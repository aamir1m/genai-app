import os
from dotenv import load_dotenv

# Load the base .env file
load_dotenv()

class Config:
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

