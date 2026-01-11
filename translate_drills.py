#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
排球训练内容AI翻译工具
使用Gemini API将训练数据翻译为中英对照格式
"""

import json
import os
import time
import re
from pathlib import Path
from google import genai

# 配置
INPUT_FILE = Path(__file__).parent / "output" / "drills_data.json"
OUTPUT_FILE = Path(__file__).parent / "constants_translated.ts"
PROGRESS_FILE = Path(__file__).parent / "translation_progress.json"

# 排球专业术语表 - 确保翻译一致性
VOLLEYBALL_GLOSSARY = {
    # 基础技术
    "passing": "垫球",
    "forearm pass": "下手垫球",
    "overhead pass": "上手传球",
    "setting": "二传/传球",
    "serve": "发球",
    "serve receive": "接发球",
    "hitting": "扣球",
    "attack": "进攻",
    "spike": "扣杀",
    "defense": "防守",
    "dig": "救球/防守起球",
    "blocking": "拦网",
    "block": "拦网",
    
    # 位置
    "setter": "二传手",
    "outside hitter": "主攻手",
    "opposite": "接应二传",
    "middle blocker": "副攻手",
    "libero": "自由人",
    "back row": "后排",
    "front row": "前排",
    
    # 场地
    "court": "场地",
    "10-foot line": "三米线/进攻线",
    "end line": "底线",
    "sideline": "边线",
    "net": "球网",
    
    # 动作
    "approach": "助跑",
    "footwork": "步法",
    "platform": "垫球平台/手臂平面",
    "ready position": "准备姿势",
    "shuffle": "滑步",
    "transition": "转换",
    "rotation": "轮转",
    
    # 训练术语
    "drill": "训练",
    "warm-up": "热身",
    "pepper": "对练",
    "free ball": "送球",
    "down ball": "轻吊/立攻",
    "tip": "吊球",
    "roll shot": "轻抹球",
    "reps": "重复次数",
    "rally": "回合",
}

# AI 翻译提示
TRANSLATION_PROMPT = """你是一位专业的排球教练和翻译专家。请将以下排球训练内容翻译成中文，要求：

1. **专业性**：使用标准的排球专业术语
2. **教练口吻**：语气权威、专业，像资深教练在讲解
3. **格式**：保持中英文对照，英文在前，中文在后
4. **准确性**：技术动作描述必须准确

专业术语参考：
- passing → 垫球
- setting → 传球
- hitting/spike → 扣球
- serve receive → 接发球
- dig → 防守起球
- platform → 垫球平台
- 10-foot line → 三米线
- transition → 转换
- rally → 回合

请翻译以下JSON数据，返回完整的翻译后JSON：

```json
{data}
```

只返回翻译后的JSON，不要添加其他说明。"""

def load_progress():
    """加载翻译进度"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "translations": {}}

def save_progress(progress):
    """保存翻译进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def translate_drill(client, drill: dict) -> dict:
    """翻译单个训练"""
    
    # 构建需要翻译的数据
    to_translate = {
        "title": drill.get("title", ""),
        "description": drill.get("description", ""),
        "setup": drill.get("setup", {}),
        "steps": drill.get("steps", []),
        "variations": drill.get("variations", []),
        "coaching_tips": drill.get("coaching_tips", [])
    }
    
    prompt = TRANSLATION_PROMPT.format(data=json.dumps(to_translate, ensure_ascii=False, indent=2))
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )
        
        # 提取JSON
        text = response.text
        
        # 清理可能的markdown代码块
        text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
        text = text.strip()
        
        translated = json.loads(text)
        
        # 合并翻译结果 - 创建中英对照
        result = drill.copy()
        result["title_cn"] = translated.get("title", "")
        result["description_cn"] = translated.get("description", "")
        result["setup_cn"] = translated.get("setup", {})
        result["steps_cn"] = translated.get("steps", [])
        result["variations_cn"] = translated.get("variations", [])
        result["coaching_tips_cn"] = translated.get("coaching_tips", [])
        
        return result
        
    except Exception as e:
        print(f"    翻译错误: {e}")
        return None

def generate_typescript(drills: list) -> str:
    """生成双语TypeScript文件"""
    
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
    
    drills_json = json.dumps(drills, ensure_ascii=False, indent=2)
    ts_content += drills_json + ";\n"
    
    return ts_content

def main():
    print("=" * 60)
    print("排球训练内容AI翻译工具")
    print("=" * 60)
    
    # 检查API密钥
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n⚠ 未找到 GEMINI_API_KEY 环境变量")
        print("请设置: set GEMINI_API_KEY=your_api_key")
        return
    
    # 初始化客户端
    print("\n[1/4] 初始化 Gemini API...")
    client = genai.Client(api_key=api_key)
    print("✓ API 初始化成功")
    
    # 读取数据
    print("\n[2/4] 读取训练数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        drills = json.load(f)
    print(f"✓ 读取 {len(drills)} 个训练")
    
    # 加载进度
    progress = load_progress()
    completed_slugs = set(progress.get("completed", []))
    translations = progress.get("translations", {})
    
    print(f"  已完成: {len(completed_slugs)} / {len(drills)}")
    
    # 翻译
    print(f"\n[3/4] 开始翻译 (每次请求间隔2秒)...")
    
    translated_drills = []
    
    for i, drill in enumerate(drills):
        slug = drill.get("slug", "")
        
        if slug in completed_slugs:
            # 使用已翻译的结果
            translated_drills.append(translations[slug])
            continue
        
        print(f"  [{i+1}/{len(drills)}] 翻译: {slug[:40]}...", end=" ", flush=True)
        
        result = translate_drill(client, drill)
        
        if result:
            translated_drills.append(result)
            translations[slug] = result
            completed_slugs.add(slug)
            
            # 保存进度
            progress["completed"] = list(completed_slugs)
            progress["translations"] = translations
            save_progress(progress)
            
            print("✓")
        else:
            # 保留原始数据
            translated_drills.append(drill)
            print("✗ (保留原文)")
        
        # 速率限制
        time.sleep(2)
    
    # 生成文件
    print(f"\n[4/4] 生成 TypeScript 文件...")
    ts_content = generate_typescript(translated_drills)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"✓ 生成 {OUTPUT_FILE}")
    
    # 统计
    cn_count = sum(1 for d in translated_drills if d.get("title_cn"))
    
    print("\n" + "=" * 60)
    print("翻译完成!")
    print("=" * 60)
    print(f"• 总训练数: {len(translated_drills)}")
    print(f"• 已翻译: {cn_count}")
    print(f"• 未翻译: {len(translated_drills) - cn_count}")
    print(f"\n输出文件: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
