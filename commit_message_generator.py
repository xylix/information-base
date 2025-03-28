# Source for initial code: 
# https://github.com/abi/autocommit/blob/main/scan_repo.py
# https://github.com/abi/autocommit/blob/main/autocommit/llm.py
# requirements: pygit2, markdown, requests, jsonl, json-repair

from collections import namedtuple
import pygit2
import requests
import json
import jsonlines
import logging
import time
from json_repair import repair_json

def generate_suggestions(commit: str) -> str:
    data = {"prompt": """<start_of_turn>user
            What follows '-------' is a git diff for a potential commit.
            End your reply with a json in this form: descriptions: [<five different possible commit messages>],
            different Git commit messages (a Git commit message should be concise but also
            try to describe the important changes in the commit), order the list by what you think
            would be the best commit message first.
            -------
            """ +commit + """
            ------
            descriptions: 
            <end_of_turn>
            <start_of_turn>model
            """,
        "n_predict": 128
    }

    r = requests.post('http://localhost:8080/completion', headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return(r.json()["content"])



# GIT_REPO_URL = os.getenv("GIT_REPO_URL")
# if GIT_REPO_URL is None:
#     raise ValueError("GIT_REPO_URL is not set")

# temp_repo_dir = "/tmp/ai-commit-msg-repo"
 
# Delete the directory if it exists
# if os.path.exists(temp_repo_dir):
#     shutil.rmtree(temp_repo_dir)

# Clone the repository
# git.Repo.clone_from(GIT_REPO_URL, temp_repo_dir)

repo = pygit2.Repository("/Users/xylix/logseq-database")
commits = repo.walk(repo.head.target, pygit2.GIT_SORT_TIME)

# Iterate over the commits and organize the data we need
commit_objects = []
CommitObject = namedtuple("CommitObject", ["sha", "message", "diff"])
for commit in commits:
    if len(commit.parents) > 0:
        diff = repo.diff(commit.parents[0], commit).patch
    else:
        diff = ""
    commit_objects.append(CommitObject(commit.id, commit.message, diff))

filtered_commit_objects = commit_objects

# edit this to start from middle (check if a duplicate was added due to this)
iteration = 0
json_error_count = 0
total_time = 0
for i in range(len(filtered_commit_objects)):
    start = time.time()

    commit = filtered_commit_objects[iteration]
    iteration = iteration + 1
    message = commit.message.replace("\n", ";")

    if str(commit.sha) == "bce07c473be7a2a8882bf2a808e3c8af4faa40c7":
        print("Arrived at commit bce07c473be7a2a8882bf2a808e3c8af4faa40c7, we're done!")
        break

    # Skip merge commits
    if message.startswith("Merge"):
        continue

    # Use 11k characters of input, which should fit into 12k context window size when running 2 scripts in parallel
    llm_start= time.time()
    raw_model_output= generate_suggestions(commit.diff[:1000])
    llm_end= time.time()
    try:
        suggestions = json.loads(raw_model_output)
    except Exception as e:
        try:
            # Sometimes there is a missing string close and ] because the model runs 
            # out of tokens before it closes the list
            logging.error(f"json loading error {e}, when trying to json.loads {raw_model_output} trying repair_json {e}")
            suggestions = repair_json(raw_model_output)
        except Exception as e_2:
            logging.error(f"exception {e_2} when trying repair_json")

            suggestions = raw_model_output
            json_error_count = json_error_count + 1

    output_item = {
        "commit": str(commit.sha),
        "descriptions": suggestions,
        "iteration": iteration,
    }

    with open("commit_generator_output.jsonl", 'a') as f:
        writer = jsonlines.Writer(f)
        writer.write(output_item)
    end = time.time()
    total_time = total_time + (end - start)
    print(f"iteration {iteration} time: {end - start}. Spent in LLM request: {llm_end - llm_start}")
    print(f"total time at iteration {total_time}")

print(f"json error frequency: {json_error_count} / {iteration} = {json_error_count / iteration}")
