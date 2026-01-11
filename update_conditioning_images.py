#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新 conditioning.js 使用 ACE 官方图片
"""

import json

# 读取图片映射
with open("output/ace_fitness/image_map.json", "r", encoding="utf-8") as f:
    image_map = json.load(f)

print(f"加载 {len(image_map)} 个图片映射")

# 读取转换后的数据
with open("output/ace_fitness/exercises_bilingual.json", "r", encoding="utf-8") as f:
    exercises = json.load(f)

print(f"加载 {len(exercises)} 条训练数据")

# 更新图片路径
updated = 0
for exercise in exercises:
    exercise_id = exercise.get('id', '')
    if exercise_id in image_map:
        exercise['image'] = image_map[exercise_id]
        updated += 1
    else:
        # 使用默认图片
        exercise['image'] = "/public/images/conditioning/default.jpg"

print(f"更新 {updated} 条图片路径")

# 生成 JS 文件
js_content = "module.exports = [\n"
for i, item in enumerate(exercises):
    js_content += "  " + json.dumps(item, ensure_ascii=False, separators=(',', ':'))
    if i < len(exercises) - 1:
        js_content += ","
    js_content += "\n"
js_content += "];\n"

with open("data/conditioning.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"\n✅ conditioning.js 已更新!")
print(f"   数据量: {len(exercises)} 条")
print(f"   文件大小: {len(js_content) / 1024:.1f} KB")
