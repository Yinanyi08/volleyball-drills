"""
合并排球专项体能和ACE通用体能数据
"""

import json

# 读取现有的排球专项数据
with open('data/conditioning.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # 提取 module.exports = [...] 中的数组
    start = content.find('[')
    end = content.rfind(']') + 1
    volleyball_data = json.loads(content[start:end].replace("'", '"'))

# 读取ACE数据
with open('data/conditioning_ace.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    ace_data = json.loads(content[start:end])

print(f"排球专项数据: {len(volleyball_data)} 条")
print(f"ACE通用数据: {len(ace_data)} 条")

# 统一分类
# 现有分类: 爆发力, 灵敏, 核心稳定, 耐力, 柔韧性, 力量
# ACE分类: 力量, 核心稳定, 柔韧性

# 为ACE数据添加标记
for item in ace_data:
    item['source'] = 'ace'
    # 调整分类名称
    if item['category'] == '柔韧性':
        item['category'] = '柔韧'

for item in volleyball_data:
    item['source'] = 'volleyball'

# 合并数据，排球专项在前
merged = volleyball_data + ace_data

# 统计分类
categories = {}
for item in merged:
    cat = item['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\n分类统计:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

# 生成最终的 conditioning.js
output = "module.exports = [\n"

for i, item in enumerate(merged):
    # 清理不需要的字段
    if 'source' in item:
        del item['source']
    
    output += "  " + json.dumps(item, ensure_ascii=False, indent=4).replace('\n', '\n  ')
    if i < len(merged) - 1:
        output += ","
    output += "\n"

output += "];\n"

with open('data/conditioning_merged.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✅ 合并完成: data/conditioning_merged.js")
print(f"   总计: {len(merged)} 条训练数据")
