import requests
from dotenv import load_dotenv

import os

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/models/openai/gpt-oss-20b/endpoints"

headers = {
    "Authorization": "Bearer $openrouter_api_key"
}

response = requests.get(url, headers=headers)

print(response.json())
