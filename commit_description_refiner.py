import requests
import json
from json_repair import repair_json
import jsonlines


def refine_suggestions(description_line: dict) -> str:
    # parsed_line: dict = repair_json(description_line)
    descriptions: list[str] | None = description_line.get("descriptions")
    if not descriptions:
        return ""
    data = {
        "prompt": """By utilizing the list of descriptions between --- and ---, write a good, 120 character description. Try to keep subjects, persons and company names, if at all possible. Respond only with a description:
        ---"""
        + str(descriptions) + "---",
        "n_predict": 144,

    }
    r = requests.post('http://localhost:8080/completion', headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return r.json()["content"]

def process_line(line: dict, out_f: jsonlines.Writer):
    new_description = refine_suggestions(line)
    new_description = new_description.replace("\n", "").replace("[", "").replace("]", "").replace('"', "")
    del line["descriptions"] 
    line["description"] = new_description
    print(line)
    out_f.write(line)

# with jsonlines.open('commit_polisher_output.jsonl', 'r') as in_f:
#     with jsonlines.open("selected_description_output.jsonl", "a", flush=True) as out_f:
#         for line in in_f:
#             process_line(line, out_f)
# 

with jsonlines.open('./commit_polisher_output_2.jsonl', 'r') as in_f:
    with jsonlines.open("selected_description_output_2.jsonl", "a", flush=True) as out_f:
        for line in in_f:
            process_line(line, out_f)


