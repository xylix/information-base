# Source for initial code: 
# https://github.com/abi/autocommit/blob/main/scan_repo.py
# https://github.com/abi/autocommit/blob/main/autocommit/llm.py
# requirements: pygit2, markdown, llama-cpp-python, jsonl

from collections import namedtuple
import sys
import pygit2
import requests
import json
import jsonlines
import logging

def generate_suggestions(commit: str) -> str:
    data = {"prompt": """What follows '-------' is a git diff for a potential commit.
            End your reply with a json in this form: descriptions: [<five different possible commit messages>],
            different Git commit messages (a Git commit message should be concise but also
            try to describe the important changes in the commit), order the list by what you think
            would be the best commit message first.
            -------
            """ +commit + """
            ------
            descriptions: 

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
iteration = 212
json_error_count = 0
for i in range(len(filtered_commit_objects)):
    commit = filtered_commit_objects[iteration]
    iteration = iteration + 1
    message = commit.message.replace("\n", ";")

    # Skip merge commits
    if message.startswith("Merge"):
        continue

    # text-davinci-003 supports 4000 tokens. Let's use upto 3500 tokens for the prompt.
    # 3500 tokens = 14,000 characters (https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
    # But in practice, > 7000 seems to exceed the limit
    raw_model_output= generate_suggestions(commit.diff[:4000])
    try:
        suggestions = json.loads(raw_model_output)
    except Exception as e:
        logging.error(f"Exception {e} when trying to json.loads {raw_model_output}")
        suggestions = raw_model_output
        json_error_count = json_error_count + 1

    output_item = {
        "commit": str(commit.sha),
        "descriptions": suggestions,
        "iteration": iteration,
    }

    with open("commit_polisher_output.jsonl", 'a') as f:
        writer = jsonlines.Writer(f)
        writer.write(output_item)

print(f"json error frequency: {json_error_count} / {iteration} = {json_error_count / iteration}")
