import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import time

endpoint = os.getenv("ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

# Get response using the code_interpreter tool
response = client.responses.create(
  model=deployment_name,
  instructions="You are an AI assistant that provides information. Use the python tool to run code for math problems.",
  input="What is the square root of 16?",
  tools=[{
    "type": "code_interpreter",
    "container": {"type": "auto"}
  }]
)

print(f"Code Interpreter Response: {response.output_text}")
print(f"Code Interpreter Raw Response: {response.output[0]}")

# Get response using the web_search tool
response = client.responses.create(
    model=deployment_name,
    instructions="You are an AI assistant. Use web search when current information is required.",
    input="What are three major announcements from Microsoft Build this week?",
    tools=[{"type": "web_search"}]
)

print(f"Web Search Response: {response.output_text}")
print(f"Web Search Raw Response: {response.output[0]}")

# Create vector store and upload a file
# vector_store = client.vector_stores.create(name="policy-docs")
# client.vector_stores.files.upload_and_poll(
#     vector_store_id=vector_store.id,
#     file=open("expenses_policy.pdf", "rb")
# )

# Get response using the file_search tool
# response = client.responses.create(
#     model=deployment_name,
#     instructions="You are an AI assistant that provides information from HR policy documents.",
#     input="What's the maximum amount I can claim for a taxi ride?",
#     tools=[{
#         "type": "file_search",
#         "vector_store_ids": [vector_store.id]
#     }],
#     include=["file_search_call.results"]
# )

# Get the time
def get_time():
    return f"The time is {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"

# 1. El modelo determina que necesita llamar a la función 
function_tools = [{
        "type": "function",
        "name": "get_time",
        "description": "Returns the current time",
}]

# Initialize messages with a system prompt
messages = [
  {"role": "developer", "content": "You are an AI assistant that provides information."},
]

response = client.responses.create(
    model=deployment_name,
    instructions="You are an AI assistant that provides information.",
    input="What is the current time?",
    tools=function_tools
)

# Loop until the user types 'quit'
while True:
        prompt = input("\nEnter a prompt (or type 'quit' to exit)\n")
        if prompt.lower() == "quit":
            break

        # Append the user prompt to the messages
        messages.append({"role": "user", "content": prompt})

        # Get initial response
        response = client.responses.create(
            model=deployment_name,
            input=messages,
            tools=function_tools
        )

        # Append model output to the messages
        messages += response.output

        # Was there a function call?
        for item in response.output:
            if item.type == "function_call" and item.name == "get_time":
                current_time = get_time()
                messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": current_time
                })

                # Get a follow up response using the tool output
                response = client.responses.create(
                    model=deployment_name,
                    instructions="Answer only with the tool output.",
                    input=messages,
                    tools=function_tools
                )

        print(f"Function Calling Response: {response.output_text}")