import json
import os

with open('output/ace_fitness/exercises_full.json', 'r', encoding='utf-8') as f:
    cond = json.load(f)

missing = []
for ex in cond:
    id_num = ex['id'].split('-')[0]
    path = f'public/images/conditioning/{id_num}.jpg'
    if not os.path.exists(path):
        missing.append(ex['id'])

print(f"Total missing: {len(missing)}")
print(missing)
