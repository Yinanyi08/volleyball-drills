#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复 drills.js 图片路径 - 匹配实际存在的文件
"""

import json
import os

# 读取原始数据
with open("output/drills_data.json", "r", encoding="utf-8") as f:
    drills = json.load(f)

# 获取实际存在的图片文件
image_dir = "public/images/drills"
existing_images = {}
for filename in os.listdir(image_dir):
    # 提取不带扩展名的文件名
    name_without_ext = os.path.splitext(filename)[0]
    existing_images[name_without_ext] = filename

print(f"找到 {len(existing_images)} 张图片")

# 匹配图片
matched = 0
unmatched = []

for drill in drills:
    slug = drill.get("slug", "default")
    
    # 查找匹配的图片
    if slug in existing_images:
        drill["image"] = f"/public/images/drills/{existing_images[slug]}"
        matched += 1
    else:
        # 尝试模糊匹配
        found = False
        for img_name, img_file in existing_images.items():
            if slug in img_name or img_name in slug:
                drill["image"] = f"/public/images/drills/{img_file}"
                matched += 1
                found = True
                break
        
        if not found:
            # 使用默认图片
            drill["image"] = "/public/images/drills/perfect-passes.jpg"
            unmatched.append(slug)
    
    # 确保有 id 和其他必要字段
    if "id" not in drill:
        drill["id"] = slug
    if "category" not in drill:
        drill["category"] = "Other"
    if "phase" not in drill:
        drill["phase"] = "技术"
    if "ageGroup" not in drill:
        drill["ageGroup"] = drill.get("age_groups", ["beginner", "intermediate"])

# 生成 JS 文件
js_content = "module.exports = " + json.dumps(drills, ensure_ascii=False, indent=2) + ";\n"

with open("data/drills.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ drills.js 已修复")
print(f"   匹配成功: {matched} 个")
print(f"   未匹配: {len(unmatched)} 个")

if unmatched:
    print(f"   未匹配的训练: {unmatched[:10]}...")
