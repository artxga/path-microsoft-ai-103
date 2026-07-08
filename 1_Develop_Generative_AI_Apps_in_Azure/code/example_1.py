import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    instructions="You are a helpful AI assistant that answers questions as a cat",
    input="What is the capital of France?",
    temperature=0.9,
    max_output_tokens=200
)

print(f"Answer: {response.output[0]}")
print(f"Response: {response.output_text}")
print(f"Response ID: {response.id}")
print(f"Tokens: {response.usage}")
print(f"Status: {response.status}")