#from azure.core.credentials import AzureKeyCredential
#from azure.search.documents import SearchClient

import sys
import openai
import asyncio
import os
import time

from dotenv import load_dotenv

async def get_completion(scores, model="gpt-3.5-turbo"):

    messages = [{
        "role": "user",
        "content": '''You are a helpful college major assessment chat bot. You will be supplied with 6 numbers in the format
R:
I:
A:
S:
E:
C:

These numbers corresspond to RIASES scores in the holland code caeer assessment text. Output five college majors based on the RIASES scores. Do not say anythig but the recommended majors.
The scores are: 

R: {}
I: {}
A: {}
S: {}
E: {}
C: {}
'''.format(scores["R"], scores["I"], scores["A"], scores["S"], scores["E"], scores["C"]) 
        }]

    response = await openai.ChatCompletion.acreate(
            model = model,
            messages=messages,
            temperature= 0
            );

    return response.choices[0].message["content"]


async def main():
    if len(sys.argv) != 7:
         print("Incorrect Amount of arguments")
         exit()

    load_dotenv()

    #service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    #index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    #key = os.environ["AZURE_SEARCH_API_KEY"]

    #search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    openai.api_key = os.environ["OPENAI_AUTH_KEY"]

    scores = {
            "C": sys.argv.pop(),
            "E": sys.argv.pop(),
            "S": sys.argv.pop(),
            "A": sys.argv.pop(),
            "I": sys.argv.pop(),
            "R": sys.argv.pop(),
        }

    response = await  get_completion(scores)

    print(response)
    

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

