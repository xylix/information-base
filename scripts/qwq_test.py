## Just a small api test to try out QWQ draft and non-draft models

import requests
import json

url = "http://localhost:8080/completion"

payload = {
    "n_predict": 384,
    "prompt": """
    <|im_start|>user 
    solution for horse + donkey = 
    <|im_end> 
    <|im_start>assistant
    """,
    "stream": True
}

headers = {"content-type": "application/json"}

s = requests.Session()

output = ""
iter = 0
with s.post(url, json=payload, headers=headers, stream=True) as resp:
    for line in resp.iter_lines():
        if line:
            decoded_line=line.decode('UTF-8')
            parsed_line = str(decoded_line.replace("data: ", ""))
            data = json.loads(parsed_line)
            output = output + data["content"]
            print(output)
