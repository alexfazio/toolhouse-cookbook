import json
import ollama
import requests

def search_web(query: str) -> str:
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-api-key': '32d520b3-b8ee-4fad-88a6-18fec4b50ad6',
    }
    data = {
        "query": query,
        "type": "neural",
        "useAutoprompt": True,
        "numResults": 10,
        "contents": {
            "text": True
        }
    }
    response = requests.post('https://api.exa.ai/search', headers=headers, json=data)
    
    try:
        response.raise_for_status()
        return json.dumps(response.json())
    except (requests.exceptions.HTTPError, json.JSONDecodeError) as e:
        return json.dumps({'error': str(e)})

def run(model: str):
    client = ollama.Client()
    messages = [{'role': 'user', 'content': 'Search the web for "current weather in New York"'}]

    response = client.chat(
        model=model,
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'search_web',
                    'description': 'Search the web for a given query',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'The search query',
                            },
                        },
                        'required': ['query'],
                    },
                },
            },
        ],
    )

    messages.append(response['message'])

    if response['message'].get('tool_calls'):
        for tool in response['message']['tool_calls']:
            function_response = search_web(tool['function']['arguments']['query'])
            messages.append({
                'role': 'tool',
                'content': function_response,
            })

    final_response = client.chat(model=model, messages=messages)
    print(final_response['message']['content'])

if __name__ == "__main__":
    run('llama3.1')