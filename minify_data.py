#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
极致压缩数据文件
通过缩写字段名来减小体积
"""

import json
import os

def minify_conditioning():
    with open("data/conditioning.js", "r", encoding="utf-8") as f:
        content = f.read()
        start = content.find('[')
        end = content.rfind(']') + 1
        data = json.loads(content[start:end])
    
    # 字段映射
    # i: id, t: title, d: description, c: category, n: intensity, g: ageGroup, m: image
    # s: setup (e: equipment, p: players, u: court)
    # st: steps, ct: coachingTips, v: variations
    
    minified = []
    for item in data:
        mini = {
            "i": item.get("id"),
            "t": item.get("title"),
            "d": item.get("description")[:100] + "..." if len(item.get("description", "")) > 100 else item.get("description"),
            "c": item.get("category"),
            "n": item.get("intensity"),
            "g": item.get("ageGroup"),
            "m": item.get("image"),
            "s": {
                "e": item.get("setup", {}).get("equipment"),
                "p": item.get("setup", {}).get("players"),
                "u": item.get("setup", {}).get("court")
            },
            "st": [s[:100] + "..." if len(s) > 100 else s for s in item.get("steps", [])][:2], # 只保留前两步
            "ct": item.get("coachingTips", []),
            "v": item.get("variations", [])
        }
        minified.append(mini)
    
    js_content = "module.exports = " + json.dumps(minified, ensure_ascii=False, separators=(',', ':')) + ";"
    with open("data/conditioning.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Conditioning minified: {len(js_content)/1024:.1f} KB")

def minify_drills():
    with open("data/drills.js", "r", encoding="utf-8") as f:
        content = f.read()
        start = content.find('[')
        end = content.rfind(']') + 1
        data = json.loads(content[start:end])
    
    minified = []
    for item in data:
        mini = {
            "i": item.get("id"),
            "t": item.get("title"),
            "d": item.get("description"),
            "c": item.get("category"),
            "p": item.get("phase", "技术"),
            "g": item.get("ageGroup"),
            "m": item.get("image"),
            "s": item.get("setup"),
            "st": item.get("steps"),
            "v": item.get("variations"),
            "ct": item.get("coaching_tips")
        }
        minified.append(mini)
    
    js_content = "module.exports = " + json.dumps(minified, ensure_ascii=False, separators=(',', ':')) + ";"
    with open("data/drills.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Drills minified: {len(js_content)/1024:.1f} KB")

if __name__ == "__main__":
    minify_conditioning()
    minify_drills()
