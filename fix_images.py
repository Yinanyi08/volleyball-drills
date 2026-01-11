import json
import os

# 使用更加稳定的 jsDelivr CDN，直接加速 GitHub 资源
CDN_BASE = "https://cdn.jsdelivr.net/gh/zyn1008/volleyball-drills/public"

def update_paths(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON part
    start = content.find('[')
    end = content.rfind(']') + 1
    json_str = content[start:end]
    data = json.loads(json_str)
    
    for item in data:
        img_path = item.get('image', '')
        # 如果是旧的 github raw 链接或者是本地路径，都统一更新为 jsDelivr
        if 'raw.githubusercontent.com' in img_path or not img_path.startswith('http'):
            # 提取文件名部分
            filename = img_path.split('/')[-1]
            if 'conditioning' in file_path:
                item['image'] = f"{CDN_BASE}/images/conditioning/{filename}"
            else:
                item['image'] = f"{CDN_BASE}/images/drills/{filename}"

    new_content = f"module.exports = {json.dumps(data, ensure_ascii=False, indent=2)};"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully optimized {file_path} with jsDelivr CDN.")

if __name__ == "__main__":
    update_paths('data/drills.js')
    update_paths('data/conditioning.js')
