import datetime
import requests
import json
from json_repair import repair_json
import time


def describe_url(url: str):
    # parsed_line: dict = repair_json(description_line)
    data = {
        "prompt": """<start_of_turn>user 
        Give one of the following categories for the link that follows, or suggest a new category. Also estimate the probability that the category is correct. For example if there is no data in the link to figure out a category from, estimate a low probability. Output a json object in the form {"topic": topic, "category": category, "p": probability}. At the end output a json list of new categories, or an empty list.
    Initial categories: ["self_improvement", "relationships", "university_courses", "scientific_research", "artificial_intelligence", "job_searches", "hobbies", "rationality", "effective_altruism", "societal_analysis", job_searches, artifial_intelligence, aviation, programming, careers, business, tech_careers, finland_specific_services, "Finnish news", media_criticism, politics, game_development, political_analysis, "political_forecasting", "self_hosting", "technology_news", "LLM_tools", "cybersecurity", "AI governance", "distributed_computing", "decision_making", sexuality, "government_policy" "gaming_strategy", "news", "gaming", "economics", "medical_tests", "cryptocurrency_economics", "computer_science", "university_courses", "politics","relationships", "government_publications", TODO]
    url:
        ---
        """
        + url + "---<end_of_turn>\n<start_of_turn>model\n",
        "n_predict": 144,

    }
    r = requests.post('http://localhost:8080/completion', headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return r.json()["content"]

with open('url_metadata.txt', 'a') as f:
    f.write(f"\n--- batch separator, time: {datetime.datetime.now()} ---\n")

with open('./start_data.txt', 'r') as f:
    urls= f.readlines()


total_time = 0
iteration = 0
for url in urls:
    start = time.time()
    iteration = iteration + 1
    response: list[dict | list] = repair_json(describe_url(url), return_objects=True)
    print(f"Parsed model output: {response}")
    response[0]["url"] = url.replace("\n", "")
    end = time.time()
    total_time = total_time + (end - start)
    print(f"iteration {iteration} total_time {total_time}")
    with open('url_metadata.txt', 'a') as f:
        f.write(str(response))
        f.write("\n")

