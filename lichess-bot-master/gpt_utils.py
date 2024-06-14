import json
import os
import re

import openai

ERRORS = (openai.RateLimitError, openai.APIError)
OpenAIObject = dict

openai.api_key = os.environ['OPENAI_API_KEY']

SYSTEM_MESSAGE = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture."


def extract_json(json_string: str):
    print("Extracting the Json")
    try:

        first_brace = json_string.index('{')
        last_brace = len(json_string) - json_string[::-1].index('}')

        return json.loads(json_string[first_brace:last_brace])

    except:
        print(json_string)


def request(prompt: str, **kwargs):
    # Just try 10 times incase we get an unexpected exception
    for _ in range(10):
        try:
            response = openai.chat.completions.create(model='gpt-4-0125-preview', messages=prompt, top_p=0,
                                                      temperature=0.0)
            return response.choices[0].message.content
        except:
            pass

    raise Exception("Failed to query OpenAPI 10 times")


def query_gpt(prompt):
    request_prompt = [{'role': 'system',
                       'content': SYSTEM_MESSAGE},
                      {'role': 'user',
                       'content': prompt}]
    output = request(request_prompt)
    return output