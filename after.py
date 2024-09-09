!pip install toolhouse openai --quiet

import nest_asyncio
from openai import OpenAI
from toolhouse import Toolhouse
from IPython.display import display, HTML

nest_asyncio.apply()

th = Toolhouse(access_token='3e76c9b1-427e-4df6-ace8-7b86a03e776b', provider="openai")
available_tools = th.get_tools()

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1"

messages = [{"role": "user", "content": "Search the web for current weather in New York using exa_web_search"}]

response = client.chat.completions.create(model=MODEL, messages=messages, tools=available_tools)
messages += th.run_tools(response)

final_response = client.chat.completions.create(model=MODEL, messages=messages, tools=available_tools)

if final_response.choices and final_response.choices[0].message.content:
    display(HTML(f"<pre>{final_response.choices[0].message.content}</pre>"))
else:
    print("No response content found.")