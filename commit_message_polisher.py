# Source for initial code: 
# https://github.com/abi/autocommit/blob/main/scan_repo.py
# https://github.com/abi/autocommit/blob/main/autocommit/llm.py
# requirements: pygit2, markdown, llama-cpp-python

from collections import namedtuple
import csv
import sys
import pygit2
from llama_cpp import Llama, LlamaGrammar
from json import loads

# from autocommit.llm import generate_suggestions

llm = Llama(
    model_path="/Users/xylix/Code/models/gemma-3-12b-it-Q8_0.gguf", 
    n_ctx=4096,
    verbose=False,)

with open("./commit_suggestion_schema.json", "r") as f:
    json_schema = f.read()
# grammar = LlamaGrammar.from_json_schema(json_schema)
# print(f"Loaded GRAMMAR: {str(grammar)}")

def generate_suggestions(commit: str, commit_hash: str) -> dict:
    base_prompt = """
    What follows "-------" is a git diff for a potential commit.
    Reply by filling in the json list descriptions: [<five different possible commit messages>]}, 
    different Git commit messages (a Git commit message should be concise but also 
    try to describe the important changes in the commit), order the list by what you think 
    would be the best commit message first. Only include the json in your response.
    
    
    ------- 
    """
    prompt = base_prompt + "\n" + commit + "\n-----\n" + '{"hash": { ' + str(commit_hash) + '}, descriptions: ['
    response = llm.create_completion(prompt=prompt, max_tokens=128, temperature=0.8)

    # Convert the markdown string to HTML
    try:
        json: dict = loads(str(response))
    except Exception as e:
        print(f"response had invalid json: {response}")
        print(f"error, the json should never be invalid")
        return {}

    # Use a regular expression to extract the list items from the HTML
    return json 

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

writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

iteration = 0
for commit in filtered_commit_objects:
    print(f"iteration: {iteration}")
    iteration = iteration + 1
    message = commit.message.replace("\n", ";")

    # Skip merge commits
    if message.startswith("Merge"):
        continue

    # text-davinci-003 supports 4000 tokens. Let's use upto 3500 tokens for the prompt.
    # 3500 tokens = 14,000 characters (https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
    # But in practice, > 7000 seems to exceed the limit
    suggestions = generate_suggestions(commit.diff[:2000], commit.sha)
    # print(suggestions)

    # generate CSV row
    writer.writerow(suggestions)
