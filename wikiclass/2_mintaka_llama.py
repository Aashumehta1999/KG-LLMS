'''
use vllm for mintaka test 4k
'''


import json
import os

from tqdm import tqdm
import urllib.request
import json

# url = "http://bendstar.com:8000/v1/chat/completions"
url = "http://163.220.176.91:8000/v1/chat/completions"
req_header = {
    'Content-Type': 'application/json',
}


def run_request(input_json):

    req = urllib.request.Request(url, data=input_json.encode(), method='POST', headers=req_header)
    with urllib.request.urlopen(req) as response:
        body = json.loads(response.read())
        headers = response.getheaders()
        status = response.getcode()
        return body['choices'][0]['message']['content']

def generate_txt(result_path,instruction_path):
    with open(result_path,'w') as w:
        with open(instruction_path,'r') as f:
            lines = f.readlines()
            for line in tqdm(lines, desc="Processing"):
                # line = line + "Give me a short answer ONLY, no sentence is needed. If you are not sure, say I do not know. If the answer is a number, use Roman Numerals."
                line = line + "Give me a short answer ONLY, no long sentence is needed.  If you are not sure, say I do not know."
                input_json = json.dumps({
                    "model": "meta-llama/Llama-2-70b-chat-hf",
                    "messages": [{"role": "system", "content": "You are a Knowledge Graph, answer the question. "},
                                 {"role": "user",   "content": line}],
                    "temperature": 0,
                })

                res = run_request(input_json)
                print(res)
                res = res.replace('\n','')
                w.write(res+'\n')

if __name__ == "__main__":

    # the generated text output path
    output_path = 'mintaka_res/'
    os.makedirs(output_path, exist_ok=True)

    result_path = os.path.join(output_path, 't2.llama_multihop.txt')
    instruction_path = 'mintaka/mintaka_test_question_multihop.txt'

    generate_txt(result_path,instruction_path)

print ('Finished.')