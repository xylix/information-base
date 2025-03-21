import datetime

with open('./start_data.txt', 'r') as f:
    urls= f.readlines()


from ollama import chat
from ollama import ChatResponse


base_prompt = """
Give one of the following categories for each link that follows, or suggest a new category. Also estimate the probability that the category is correct. For example if there is no data in the link to figure out a category from, estimate a low probability. Output a json list, every url having a json object in the form {"url": url, "topic": topic, "category": category, "p": probability}. At the end output a json list of new categories, or an empty list.
    Initial categories: ["self_improvement", "relationships", "university_courses", "scientific_research", "artificial_intelligence", "job_searches", "hobbies", "rationality", "effective_altruism"]
    Links:
"""

output = []

batch_start_position = 310

with open('output.txt', 'a') as f:
    f.write(f"--- batch separator, batch start {batch_start_position} time: {datetime.datetime.now()} ---")

for i in range(batch_start_position, len(urls), 10):
    print(f"Processing batch {i}")
    urls_in_batch = "\n".join(urls[i:(i+10)])

    response: ChatResponse = chat(model='gemma3:12b', messages=[
      {
        'role': 'user',
        'content': base_prompt + "\n" + urls_in_batch,
      },
    ])
    model_output = response['message']['content']
    print(model_output)
    with open('output.txt', 'a') as f:
        f.write(model_output)

