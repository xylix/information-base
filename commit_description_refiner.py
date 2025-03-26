import requests
import json
import time
import jsonlines


def refine_suggestions(description_line: dict) -> str:
    # parsed_line: dict = repair_json(description_line)
    descriptions: list[str] | None = description_line.get("descriptions")
    if not descriptions:
        return ""
    data = {
        "prompt": """<start_of_turn>user 
        By utilizing the list of descriptions between --- and ---, write a good, 120 character description. If there are human or company names in the descriptions try to keep them. If not, do not add those. Avoid unnecessary adjectives. Respond only with a description:
        ---
        """
        + str(descriptions) + "---<end_of_turn>\n<start_of_turn>model\n",
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
total_time = 0
iteration = 0
with jsonlines.open('./commit_polisher_output.jsonl', 'r') as in_f:
    with jsonlines.open("selected_commit_messages.jsonl", "a", flush=True) as out_f:
        for line in in_f:
            iteration = iteration + 1
            start = time.time()
            # old val 1395
            if line["iteration"] < 0:
                pass
            else:
                process_line(line, out_f)
            end = time.time()
            total_time = total_time + (end - start)
            print(f"iteration {iteration} total_time {total_time}")

