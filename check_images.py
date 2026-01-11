#!/usr/bin/env python
import json

with open('data/drills.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    drills = json.loads(content[start:end])

png_count = 0
jpg_count = 0
for drill in drills:
    img = drill.get('image', '')
    if '.png' in img:
        png_count += 1
        print(f'PNG: {img}')
    elif '.jpg' in img:
        jpg_count += 1

print(f'\n总计: {jpg_count} jpg, {png_count} png')

for d in drills[:3]:
    print(f"\n{d['slug']}: {d['image']}")
