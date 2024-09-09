from openai import OpenAI
from toolhouse import Toolhouse

def get_user_input():
    return input("😎 User: ")

if __name__ == "__main__":
    th = Toolhouse(access_token='3e76c9b1-427e-4df6-ace8-7b86a03e776b', provider="openai")
    th.set_metadata("timezone", -7)
    available_tools = th.get_tools()
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    MODEL = "llama3.1"
    
    while True:
        user_message = get_user_input()
        if user_message.lower() == 'quit':
            break
        
        messages = [{"role": "user", "content": user_message}]
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=available_tools)
        messages += th.run_tools(response)
        final_response = client.chat.completions.create(model=MODEL, messages=messages, tools=available_tools)
        
        if final_response.choices and final_response.choices[0].message.content:
            print("AI response:", final_response.choices[0].message.content)
        else:
            print("No response content found.")
        
        print("\n---\n")