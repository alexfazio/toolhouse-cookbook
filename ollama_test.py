from openai import OpenAI
from toolhouse import Toolhouse
import sys

# Initialize the Toolhouse SDK
try:
    th = Toolhouse(access_token='3e76c9b1-427e-4df6-ace8-7b86a03e776b', provider="openai")
    print("Toolhouse SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Toolhouse SDK: {e}")
    sys.exit(1)

# Initialize the OpenAI client with Ollama's endpoint
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but unused
)
print("Ollama client initialized via OpenAI-compatible API.")

# Define the model to use
MODEL = "llama3.1"
print(f"Using model: {MODEL}")

# Define the messages to send to the model
messages = [
    {
        "role": "user",
        "content": "Generate FizzBuzz code. Execute it to show me the results up to 10."
    }
]
print(f"Initial message: {messages[0]['content']}")

# Create the completion request
try:
    print("Sending initial completion request...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=th.get_tools(),
    )
    print("Initial completion request successful.")
except Exception as e:
    print(f"Error in initial completion request: {e}")
    sys.exit(1)

# Run the remote tool and get the result
try:
    print("Running tools...")
    tool_run = th.run_tools(response)
    messages += tool_run
    print(f"Tool execution successful. Added {len(tool_run)} new message(s) to the conversation.")
except Exception as e:
    print(f"Error running tools: {e}")
    sys.exit(1)

# Create the final completion request with the updated messages
try:
    print("Sending final completion request...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=th.get_tools(),
    )
    print("Final completion request successful.")
except Exception as e:
    print(f"Error in final completion request: {e}")
    sys.exit(1)

# Print the response with the answer
if response.choices and response.choices[0].message.content:
    print("\nFinal response:")
    print(response.choices[0].message.content)
else:
    print("No response content found in the model's reply.")
    print("Response object:", response)

