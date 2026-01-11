import json
import os
import re

# New CDN Target
CDN_BASE = "https://cdn.jsdelivr.net/gh/Yinanyi08/volleyball-drills@main/public"

def update_paths(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'module\.exports\s*=\s*(\[.*\])\s*;?', content, re.DOTALL)
    if not match:
        print(f"Could not find data array in {file_path}")
        return
        
    json_str = match.group(1)
    data = json.loads(json_str)
    
    updated_count = 0
    for item in data:
        img_key = 'm' if 'm' in item else 'image' if 'image' in item else None
        if img_key:
            img_path = item[img_key]
            if img_path and img_path.startswith('http'):
                # Handle any previous GitHub or jsDelivr accounts and switch to the new one
                if 'github' in img_path or 'jsdelivr' in img_path:
                    if 'Yinanyi08' not in img_path:
                        # Extract the path after the account/repo part
                        # e.g., .../volleyball-drills@main/public/images/... -> /images/...
                        path_match = re.search(r'public(/.+)$', img_path)
                        if path_match:
                            item[img_key] = CDN_BASE + path_match.group(1)
                            updated_count += 1
                continue
            
            # Relative path logic
            if img_path:
                clean_path = img_path.replace('/public', '')
                if not clean_path.startswith('/'): clean_path = '/' + clean_path
                if clean_path.endswith('.png'): clean_path = clean_path[:-4] + '.jpg'
                item[img_key] = CDN_BASE + clean_path
                updated_count += 1

    new_json_str = json.dumps(data, ensure_ascii=False)
    new_content = f"module.exports = {new_json_str};"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {file_path}. Updated {updated_count} image paths to CDN.")

if __name__ == "__main__":
    update_paths('data/drills.js')
    update_paths('data/conditioning.js')
