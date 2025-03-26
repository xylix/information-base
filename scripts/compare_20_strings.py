import random

# Script to compare two sets of 20 strings and figure out which the user prefers

# Two sets of data with 20 lines each
dataset1 = """{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'Update workspace notes with current projects, tasks, and next steps for clear progress tracking.'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': "Detailed lecture notes on computer architecture: Amdahl's law, memory hierarchy (DRAM, SSD), performance, & error rates."}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'LM testing, DeepSeek-r1 prep & Notebook LM experiences documented. Notes on hallucinations & potential improvements added. #AI #LLM'}
{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'DeepSeek-R1 research notes added & updated for AI presentations and documentation on reasoning models.'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': "Amdahl's Law & processor performance. Lecture notes updated with key equation & metrics. Expand your understanding today."}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'Document LM testing results, including observations & issues, for the AI page. March 2025 notebook notes.'}
{'commit': 'f8fe63a7f67309e0ae373dd811a79295799834c0', 'iteration': 4, 'description': 'Expanded explanation of programming talent, aptitude, and motivation – clarifying abilities and improving discussion for clarity.'}
{'commit': '2b3b974df4ff5ff7d13c97e3af5c9bacb708c415', 'iteration': 5, 'description': 'Refactored 2025 tab: AI assistant note filtering and cleanup. Google Keep data export ignored. Improved organization.'}
{'commit': '64b078c85a8152dc29c516539506b5af43f80ec9', 'iteration': 6, 'description': 'AI-assisted 2025 note-taking: Consolidate, categorize, and search tasks. Includes Google integration & AI-driven TODOs.'}
{'commit': 'bce246afc3c296f9a8c4987f4f67667c3da9b4f5', 'iteration': 7, 'description': 'Document RAG integration challenges & potential Marqo adoption. Troubleshoot, explore open-source alternatives.'}
{'commit': '981d36c250ddffbc1c0d914bb8b69a0c6a166273', 'iteration': 8, 'description': 'Deleting the HPmor notes page to streamline documentation.'}
{'commit': 'e2f54287affc2a3a8b491015bc592f52255dcc06', 'iteration': 9, 'description': 'AI brainstorming sessions recorded, including notes on Retrieval Augmented Generation (RAG) considerations and discussions.'}
{'commit': 'b4ebc3923cdaa2a9f75265b810e7aef598ec10d1', 'iteration': 10, 'description': 'TJK training documented - operating grants & portal process. Edari updated with details & guidance for future reference.'}
{'commit': 'f013146ba893e32845b619c4ca401e501b0b2ca2', 'iteration': 11, 'description': 'Added detailed to-do list, including alert cleanup & urgent tasks. For March 16, 2025.'}
{'commit': 'ae36dd2fca4d025790dbad00bb6e60fd311d7898', 'iteration': 12, 'description': 'DeepSeek R1 now available! Added to the 2025 tab & optimized for Apple Neural Engine. Explore enhanced performance.'}
{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'DeepSeek-R1 presentation prep: added notes, docs, and research to streamline creation.'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': "Computer architecture: Explore Amdahl's Law & performance equations. Update with recent lecture notes & expanded content."}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'LM testing in notebook documented. March 2025 results & observations recorded. AI notes updated.'}
{'commit': 'f8fe63a7f67309e0ae373dd811a79295799834c0', 'iteration': 4, 'description': 'Programming aptitude: Exploring its nature, motivation, and dispelling common myths. Challenge the idea of innate talent.'}
{'commit': '2b3b974df4ff5ff7d13c97e3af5c9bacb708c415', 'iteration': 5, 'description': 'Refactored 2025 tab cleanup with AI notes, adding .gitignore & cleaning irrelevant notes. Enhanced project organization.'}"""

dataset2 = """{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'Updated workspace notes detail recent work, tasks, and progress on ongoing projects. Next steps documented.'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': "Computer architecture lecture notes: Amdahl's law, memory hierarchies (DRAM, SSDs), performance, and error correction techniques."}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'LM testing documented, DeepSeek-r1 prep notes added. Hallucinations & improvements noted for AI page update.'}
{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'DeepSeek-R1 research & reasoning models documented for presentation prep & AI notes. #AI #DeepSeek'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': "Amdahl's Law and performance equation added to lecture notes. Includes calculations and performance metrics."}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'LM testing notes from March 2025 recorded, updated AI page, and documented results. Observations & issues added.'}
{'commit': 'f8fe63a7f67309e0ae373dd811a79295799834c0', 'iteration': 4, 'description': 'Clarify & expand discussion on programming talent, aptitude & motivation; improve understanding & ability.'}
{'commit': '2b3b974df4ff5ff7d13c97e3af5c9bacb708c415', 'iteration': 5, 'description': 'Refactor 2025 tab: AI filtering & cleanup. Google Keep export ignored. Improves organization and data privacy.'}
{'commit': '64b078c85a8152dc29c516539506b5af43f80ec9', 'iteration': 6, 'description': 'AI-assisted note consolidation & task organization for 2025, leveraging Google search & TODO notes. Streamline your workflow.'}
{'commit': 'bce246afc3c296f9a8c4987f4f67667c3da9b4f5', 'iteration': 7, 'description': 'Document RAG integration challenges, explore Marqo, and plan open-source alternatives. Troubleshooting efforts recorded.'}
{'commit': '981d36c250ddffbc1c0d914bb8b69a0c6a166273', 'iteration': 8, 'description': 'Remove unused HPmor notes page for streamlined efficiency.'}
{'commit': 'e2f54287affc2a3a8b491015bc592f52255dcc06', 'iteration': 9, 'description': 'AI brainstorming session recorded, including RAG considerations and notes. Updated March 14, 2025.'}
{'commit': 'b4ebc3923cdaa2a9f75265b810e7aef598ec10d1', 'iteration': 10, 'description': 'TJK training details and operating grant guidance documented for Edari and portal.lyyti.fi. Meeting notes and session records updated.'}
{'commit': 'f013146ba893e32845b619c4ca401e501b0b2ca2', 'iteration': 11, 'description': 'Added detailed to-do list for March 16, 2025, including urgent tasks & alert cleanup.'}
{'commit': 'ae36dd2fca4d025790dbad00bb6e60fd311d7898', 'iteration': 12, 'description': 'DeepSeek R1 model info added! Now on Apple Neural Engine and the 2025 tab for easy access.'}
{'commit': 'b1c89bedb808abae4875fafb0b11144df9c413ae', 'iteration': 1, 'description': 'Added notes documenting DeepSeek-R1 presentation preparation research and content.'}
{'commit': '03e851bec954b7b54a04af4e7da55765249386f1', 'iteration': 2, 'description': 'Amdahl’s Law explained: Performance limitations & equation. Update to Computer Architecture notes, including visiting lecture details.'}
{'commit': 'ff6a3ac6c76edf9643fca6cfef8a28915a599bb7', 'iteration': 3, 'description': 'Document LM testing results & observations from March 2025, including notebook analysis.'}
{'commit': 'f8fe63a7f67309e0ae373dd811a79295799834c0', 'iteration': 4, 'description': 'Explore programming aptitude: debunk myths, understand motivation, and challenge the talent concept. Develop your skills!'}
{'commit': '2b3b974df4ff5ff7d13c97e3af5c9bacb708c415', 'iteration': 5, 'description': 'Refactored 2025 tab cleanup, added .gitignore, and updated with AI notes for a cleaner, more efficient workflow.'}"""

# Split the datasets into lists
list1 = dataset1.strip().split('\n')
list2 = dataset2.strip().split('\n')

# Make sure both lists have the same length
if len(list1) != len(list2):
    print("Error: The two datasets must have the same number of lines.")
    exit(1)

# Create pairs of items from both datasets
pairs = list(zip(list1, list2))

# Count how many items we have
total_items = len(pairs)
print(f"You'll be comparing {total_items} pairs of items.\n")

# Dictionary to store results
results = {
    "dataset1": 0,
    "dataset2": 0
}

# Shuffle the pairs to randomize the order
random.shuffle(pairs)

# Present each pair and ask for user preference
for i, (item1, item2) in enumerate(pairs):
    # Randomly decide which order to display the items
    if random.choice([True, False]):
        option1, option2 = item1, item2
        mapping = {1: "dataset1", 2: "dataset2"}
    else:
        option1, option2 = item2, item1
        mapping = {1: "dataset2", 2: "dataset1"}
    
    print(f"\nComparison {i+1} of {total_items}")
    print("-" * 40)
    print(f"Option 1: {option1}")
    print(f"Option 2: {option2}")
    print("-" * 40)
    
    # Get user input and validate it
    while True:
        choice = input("Which option do you prefer? (1/2/3): ").strip()
        if choice in ['1', '2']:
            choice = int(choice)
            results[mapping[choice]] += 1
            break
        elif choice in '3':
            pass
        else:
            print("Invalid input. Please enter 1 or 2.")

# Display final results
print("\n" + "=" * 40)
print("RESULTS:")
print(f"Dataset 1 preferred: {results['dataset1']} times")
print(f"Dataset 2 preferred: {results['dataset2']} times")

if results['dataset1'] > results['dataset2']:
    print(f"\nOverall preference: Dataset 1, ratio {results['dataset1'] / results['dataset2']}")
elif results['dataset2'] > results['dataset1']:
    print(f"\nOverall preference: Dataset 2, ratio: {results['dataset1'] / results['dataset2']}")
else:
    print("\nOverall preference: Tie")
print("=" * 40)
