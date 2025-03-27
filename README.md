Tooling for building myself an "information base" - something worse than a knowledge base but better than fragmented notes, tabs, and files everywhere.

Maybe it can eventually become a knowledge base, but for now it's the "knowledge base at home"

# What, why, how

## Motivation:
<img src="https://github.com/user-attachments/assets/b5bbb415-b62c-403d-b4c3-ebd4d3c42001" width=400>

## End goal:

- If I have a bunch of ~unorganized info, like notes, tabs, or .pdf papers, I have a semi-automated tooling workflow that can categorize, tag, and organize them.
  - So I will have to do less manual organizing, and hopefully the organizing result will be better than what I can currently achieve.
  - Currently I spend maybe 2-4 hours per month organizing notes, tabs, todos, etc., and this is not enough so I gather a growing backlog constantly, and also I don't have a good system for categorizing and tagging things.

- Specific goals for the organized notes:   
    - figuring out how my thinking and notetaking has evolved over the years
    - semantically finding old stuff from notes
    - making a semantic URL library with metadata and stuff, out of my exported tabs & bookmark folders
        -  and a scripted tool to clean up hundreds of tabs into nice note items
  
  - what needs does this serve:
    - 1: Actually being useful (compared to browsing history) in finding things that I recall reading / seeing and that seem relevant to other thing that I'm thinkign about later
    - 2: I have a lot of anxiety about "missing" things on the internet and probably the correct solution would be to just accept it and close tabs - but if I can find a stopgap with tech that's probably a better middleground than my current situation.


## url_processor.py
- A script that uses LLM models to figure out categories for

## Backlog:



to-do:

Editing logseq-database:
    - Use scripting + LLM to enrichen the data (add URL titles, fix quote blocks)


URL metadata / categorization tool:
    - Check that the tool doesn't hallucinate urls
        - [ ] prevent this by just using the url from the input and giving input line by line
    - Add a tool to the LLM so when categorizing it can check the web pages? Or do a web request + add to prompt?
        - maybe with omnitool?
    - [/] Re-run url categorization with correct temperature etc., and the set of generated categories (curated / merged by human)
        - Merge these:         - ["societal_analysis", job_searches, artifial_intelligence, aviation, programming, careers, business, tech_careers, finland_specific_services, "Finnish news", media_criticism, politics, game_development, political_analysis, "political_forecasting", "self_hosting", "technology_news", "LLM_tools", "cybersecurity", "AI governance", "distributed_computing", "decision_making", sexuality, "government_policy" "gaming_strategy", "news", "gaming", "economics", "medical_tests", "cryptocurrency_economics", "computer_science", "university_courses", "politics","relationships", "government_publications",]
            - Category ideas: "todos", yhteiskuntatiede / social sciences (for finland, us, global?), history
            - "unknown" "Data and APIs", "AI Safety", "AI in Games", "data_processing", "vector_databases", "machine_learning_tools"]


ideas:
    - utilize prompt finetuning for improved accuracy
