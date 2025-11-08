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

# curl https://openrouter.ai/api/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $OPENROUTER_API_KEY" \
#   -H "HTTP-Referer: http://localhost" \
#   -H "X-Title: Test" \
#   -d '{
#     "model": "openai/gpt-oss-20b",
#     "messages": [
#       {"role": "user", "content": "Tell me a joke"}
#     ]
#   }'
#
