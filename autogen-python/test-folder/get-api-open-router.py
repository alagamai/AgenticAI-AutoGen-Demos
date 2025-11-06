import requests

openrouter_api_key = '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'

url = "https://openrouter.ai/api/v1/models/openai/gpt-oss-20b/endpoints"

headers = {
    "Authorization": "Bearer $openrouter_api_key"
}

response = requests.get(url, headers=headers)

print(response.json())
