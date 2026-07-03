import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()
endpoint = os.getenv("ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response1 = client.responses.create(
    model=deployment_name,
    instructions="You are a helpful AI assistant that answers questions as a cat",
    input="What is machine learning?",
    temperature=0.9,
    max_output_tokens=200
)

print("Assistant:", response1.output_text)

response2 = client.responses.create(
    model=deployment_name,
    instructions="You are a helpful AI assistant that answers questions as a cat",
    input="Can you give me an example?",
    temperature=0.9,
    previous_response_id=response1.id
)

print("Assistant:", response2.output_text)