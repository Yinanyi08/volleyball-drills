import json
import re

def check_english(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'module\.exports\s*=\s*(\[.*\])\s*;?', content, re.DOTALL)
    if not match: return
    data = json.loads(match.group(1))
    
    fields_to_check = ['t', 'd', 'st', 'ct', 'v']
    english_found = []
    
    def walk(obj, field_name=None):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, k)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, field_name)
        elif isinstance(obj, str):
            if field_name not in fields_to_check:
                return
            
            # Find English words (a-z) - excluding some common units or exceptions
            # Also excluding Chinese parentheses with text inside which might match
            # But let's just look for sequences of 3+ letters
            words = re.findall(r'[A-Za-z]{3,}', obj)
            
            # Filter out some intentionally kept terms if any
            words = [w for w in words if w.lower() not in ['trx', 'ckc', 'v-ups', 'abc']]
            
            if words:
                english_found.append((field_name, obj, words))

    walk(data)
    
    if english_found:
        print(f"--- Potential English in {file_path} ---")
        for field, text, words in english_found[:15]:
            print(f"[{field}]: {text} (Found: {words})")
        print(f"Total entries with potential English: {len(english_found)}")
    else:
        print(f"✅ No significant English found in {file_path}")

if __name__ == "__main__":
    check_english('data/drills.js')
    check_english('data/conditioning.js')
