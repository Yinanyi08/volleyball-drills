import json
import re

def swap_bilingual(text):
    if not isinstance(text, str): return text
    # Match "English text... (Chinese text...)"
    # We use a non-greedy match for the first part and greedy for the one inside parentheses
    # But often there are multiple sentences. 
    # Let's try to find the last occurrence of '(' and ')'
    match = re.search(r'^(.*?)\(([^()]+)\)\s*$', text.strip())
    if match:
        eng = match.group(1).strip()
        chn = match.group(2).strip()
        # Only swap if the second part contains Chinese characters
        if any('\u4e00' <= char <= '\u9fff' for char in chn):
            return f"{chn} ({eng})"
    return text

def process():
    file_path = 'data/drills.js'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON
    start = content.find('[')
    end = content.rfind(']') + 1
    json_str = content[start:end]
    drills = json.loads(json_str)
    
    for d in drills:
        d['title'] = swap_bilingual(d.get('title', ''))
        d['description'] = swap_bilingual(d.get('description', ''))
        
        if 'setup' in d:
            for k in d['setup']:
                d['setup'][k] = swap_bilingual(d['setup'][k])
        
        if 'steps' in d:
            d['steps'] = [swap_bilingual(s) for s in d['steps']]
        
        if 'variations' in d:
            d['variations'] = [swap_bilingual(v) for v in d['variations']]
            
        if 'coachingTips' in d:
            d['coachingTips'] = [swap_bilingual(t) for t in d['coachingTips']]

    # Write back
    new_json = json.dumps(drills, ensure_ascii=False, indent=2)
    new_content = f"module.exports = {new_json};"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully swapped bilingual order in {file_path}")

if __name__ == "__main__":
    process()
