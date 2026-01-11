#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练数据转换脚本
将爬取的英文数据转换为中文并生成 constants.ts 格式
使用 Gemini API 进行翻译
"""

import json
import os
import re
import time
from pathlib import Path

# 配置
INPUT_FILE = Path(__file__).parent / "output" / "drills_data.json"
OUTPUT_FILE = Path(__file__).parent / "constants_generated.ts"
IMAGES_SRC = Path(__file__).parent / "output" / "images"
IMAGES_DEST = Path(__file__).parent / "public" / "images" / "drills"

# 技能类别映射
CATEGORY_MAP = {
    "passing": "垫球",
    "serve": "发球",
    "serving": "发球",
    "setting": "传球",
    "hitting": "扣球",
    "defense": "防守",
    "blocking": "拦网",
    "warm-up": "综合",
    "ball-control": "综合",
    "pepper": "综合",
    "down-ball": "扣球",
    "fitness": "体能",
    "offense": "综合",
    "middle-hitting": "扣球",
    "outside-hitting": "扣球",
    "pass-set-hit": "综合",
    "serve-defense": "防守"
}

# 年龄段映射
AGE_MAP = {
    "beginner": "入门",
    "intermediate": "进阶",
    "high_school": "高中",
    "advanced": "专业"
}

# 训练阶段推断
def infer_phase(title: str, category: str) -> str:
    title_lower = title.lower()
    if any(w in title_lower for w in ['warm-up', 'warm up', 'warmup']):
        return "热身"
    if any(w in title_lower for w in ['game', 'competition', 'vs', 'challenge', 'drill']):
        return "技术"
    if any(w in title_lower for w in ['serve receive', 'offense', 'transition', 'live']):
        return "实战"
    if any(w in title_lower for w in ['fitness', 'conditioning', 'endurance']):
        return "体能"
    return "技术"

# 难度推断
def infer_difficulty(age_groups: list) -> int:
    if "advanced" in age_groups:
        return 4
    if "high_school" in age_groups:
        return 3
    if "intermediate" in age_groups:
        return 2
    return 1

# 提取类别
def extract_category(slug: str, title: str) -> str:
    slug_lower = slug.lower()
    title_lower = title.lower()
    
    for key, cat in CATEGORY_MAP.items():
        if key in slug_lower or key in title_lower:
            return cat
    return "综合"

# 翻译标题映射表（常见模式）
TITLE_TRANSLATIONS = {
    "Passing": "垫球",
    "Serve Receive": "接发球",
    "Serving": "发球",
    "Setting": "传球",
    "Hitting": "扣球",
    "Defense": "防守",
    "Blocking": "拦网",
    "Warm-Up": "热身",
    "Ball Control": "控球",
    "Pepper": "对练",
    "Down Ball": "下击球",
    "Drill": "训练",
    "Challenge": "挑战",
    "Game": "对抗赛",
    "Transition": "转换",
    "Quick": "快速",
    "Partner": "双人",
    "Team": "团队",
    "Individual": "个人",
}

def translate_title(title: str) -> str:
    """简单的标题翻译"""
    result = title
    # 移除 "Volleyball" 前缀
    result = re.sub(r'^Volleyball\s+', '', result)
    result = re.sub(r'\s+Drill:?\s*', ':', result)
    
    for en, cn in TITLE_TRANSLATIONS.items():
        result = result.replace(en, cn)
    
    # 保留英文作为补充
    if result == title:
        return title
    return result

def clean_steps(steps: list) -> list:
    """清理步骤列表，移除导航内容"""
    cleaned = []
    for step in steps:
        # 跳过导航/分类链接内容
        if "Drills by Age" in step or "Drills by Skill" in step:
            continue
        if len(step) < 15:
            continue
        # 移除重复的设置信息
        if step.startswith(("Players:", "Court:", "Equipment:", "Roles:")):
            continue
        cleaned.append(step)
    return cleaned[:6]  # 最多6个步骤

def process_drill(drill: dict, index: int) -> dict:
    """处理单个训练数据"""
    slug = drill.get("slug", "")
    title = drill.get("title", "")
    description = drill.get("description", "")
    
    # 提取类别
    category = extract_category(slug, title)
    
    # 年龄组转换
    age_groups = [AGE_MAP.get(ag, ag) for ag in drill.get("age_groups", [])]
    
    # 推断阶段和难度
    phase = infer_phase(title, category)
    difficulty = infer_difficulty(drill.get("age_groups", []))
    
    # 清理步骤
    steps = clean_steps(drill.get("steps", []))
    variations = drill.get("variations", [])[:3]
    coaching_tips = drill.get("coaching_tips", [])[:3]
    
    # 设置信息
    setup = drill.get("setup", {})
    
    return {
        "url": drill.get("url", ""),
        "slug": slug,
        "title": title,  # 保留英文标题，因为中文翻译需要AI
        "description": description,
        "category": category,
        "phase": phase,
        "difficulty": difficulty,
        "duration": "10-15 分钟",
        "setup": {
            "players": setup.get("players", ""),
            "court": setup.get("court", ""),
            "equipment": setup.get("equipment", ""),
            "roles": setup.get("roles", "")
        },
        "steps": steps,
        "variations": variations,
        "coaching_tips": coaching_tips,
        "image_url": drill.get("image_url", ""),
        "local_image": f"/images/drills/{slug}.png",
        "age_groups": age_groups
    }

def generate_typescript(drills: list) -> str:
    """生成 TypeScript 常量文件"""
    
    ts_content = '''
import { Drill, SkillCategory } from './types';

export const SKILL_CATEGORIES: SkillCategory[] = [
  '垫球',
  '发球',
  '传球',
  '扣球',
  '防守',
  '拦网',
  '综合'
];

export const AGE_LEVELS = [
  { id: '入门', label: '入门组 (6-10岁)', desc: '侧重球感与基本动作' },
  { id: '进阶', label: '进阶组 (10-14岁)', desc: '侧重技术稳定性与移动' },
  { id: '高中', label: '高中组 (14-18岁)', desc: '侧重战术配合与对抗' },
  { id: '专业', label: '专业/成人组 (18+)', desc: '侧重高强度实战与专项' }
];

export const DRILLS_DATA: Drill[] = '''
    
    # 格式化 drills 数据
    drills_json = json.dumps(drills, ensure_ascii=False, indent=2)
    
    # 修复 JSON 到 TypeScript 的类型标注
    ts_content += drills_json + ";\n"
    
    return ts_content

def copy_images():
    """复制图片到 public 目录"""
    IMAGES_DEST.mkdir(parents=True, exist_ok=True)
    
    import shutil
    copied = 0
    for img in IMAGES_SRC.glob("*.png"):
        dest = IMAGES_DEST / img.name
        shutil.copy2(img, dest)
        copied += 1
    
    print(f"✓ 复制 {copied} 张图片到 {IMAGES_DEST}")

def main():
    print("=" * 60)
    print("训练数据转换工具")
    print("=" * 60)
    
    # 1. 读取数据
    print("\n[1/4] 读取爬取数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_drills = json.load(f)
    print(f"✓ 读取 {len(raw_drills)} 个训练")
    
    # 2. 处理数据
    print("\n[2/4] 处理并分类数据...")
    processed = []
    for i, drill in enumerate(raw_drills):
        processed.append(process_drill(drill, i))
    print(f"✓ 处理完成 {len(processed)} 个训练")
    
    # 统计分类
    categories = {}
    for d in processed:
        cat = d["category"]
        categories[cat] = categories.get(cat, 0) + 1
    print("  分类统计:", categories)
    
    # 3. 生成 TypeScript
    print("\n[3/4] 生成 TypeScript 文件...")
    ts_content = generate_typescript(processed)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    print(f"✓ 生成 {OUTPUT_FILE}")
    
    # 4. 复制图片
    print("\n[4/4] 复制图片...")
    copy_images()
    
    print("\n" + "=" * 60)
    print("转换完成!")
    print("=" * 60)
    print(f"\n请将 {OUTPUT_FILE.name} 重命名为 constants.ts 或将内容复制过去")

if __name__ == "__main__":
    main()
