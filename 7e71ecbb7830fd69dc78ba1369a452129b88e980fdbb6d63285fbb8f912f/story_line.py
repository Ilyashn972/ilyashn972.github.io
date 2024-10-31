import sys


line = '<li><a href="Story/">Story</a></li>'
with open('/Users/ilyashnayderman/projects/llm-narrative-analysis/story_names.txt') as f:
    for new_story_name in f:
        updated_line = line.replace("Story", new_story_name.strip())

        print(updated_line)
