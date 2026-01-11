"""
压缩体能训练数据
减少数据体积以适应小程序 2MB 限制
"""

import json
import re

def compress_data(input_file, output_file):
    """压缩数据"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据: {len(data)} 条")
    
    compressed = []
    for item in data:
        # 压缩步骤：只保留前2个步骤，每个最多200字符
        steps = []
        for step in item.get('steps', [])[:2]:
            # 截断并清理
            step = re.sub(r'\s+', ' ', step)
            if len(step) > 200:
                step = step[:197] + "..."
            steps.append(step)
        
        # 压缩描述：最多80字符
        desc = item.get('description', '')
        if len(desc) > 80:
            desc = desc[:77] + "..."
        
        compressed_item = {
            "id": item['id'],
            "title": item['title'],
            "description": desc,
            "category": item['category'],
            "intensity": item['intensity'],
            "ageGroup": ["intermediate", "advanced"],  # 简化
            "image": "/public/images/conditioning/default.png",
            "setup": item['setup'],
            "steps": steps,
            "coachingTips": [
                "保持正确姿势 (Maintain proper form)",
                "控制节奏 (Control tempo)"
            ],
            "variations": []
        }
        compressed.append(compressed_item)
    
    # 生成 JS 文件
    js_content = "module.exports = [\n"
    for i, item in enumerate(compressed):
        js_content += "  " + json.dumps(item, ensure_ascii=False, separators=(',', ':'))
        if i < len(compressed) - 1:
            js_content += ","
        js_content += "\n"
    js_content += "];\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # 计算压缩后大小
    original_size = len(open(input_file, 'r', encoding='utf-8').read())
    compressed_size = len(js_content)
    
    print(f"✅ 压缩完成!")
    print(f"   原始大小: {original_size/1024:.1f} KB")
    print(f"   压缩后: {compressed_size/1024:.1f} KB")
    print(f"   压缩率: {(1 - compressed_size/original_size)*100:.1f}%")

if __name__ == "__main__":
    compress_data(
        "output/ace_fitness/exercises_bilingual.json",
        "data/conditioning.js"
    )
