#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
下载 ACE Fitness 官方训练图片
图片格式: https://ik.imagekit.io/02fmeo4exvw/exercise-library/large/{id}-2.jpg
"""

import json
import requests
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
OUTPUT_DIR = "public/images/conditioning"
BASE_IMAGE_URL = "https://ik.imagekit.io/02fmeo4exvw/exercise-library/large"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_id_number(exercise_id):
    """从练习 ID 中提取数字部分"""
    # ID 格式: "94-forward-lunge" -> 提取 94
    match = re.match(r'^(\d+)-', exercise_id)
    if match:
        return match.group(1)
    return None

def download_image(exercise):
    """下载单个练习的图片"""
    exercise_id = exercise.get('id', '')
    id_number = extract_id_number(exercise_id)
    
    if not id_number:
        return None, f"无法提取ID: {exercise_id}"
    
    # 尝试不同的图片序号 (1, 2, 3)
    for suffix in ['2', '1', '3']:
        image_url = f"{BASE_IMAGE_URL}/{id_number}-{suffix}.jpg"
        
        try:
            response = requests.get(image_url, timeout=15)
            if response.status_code == 200 and len(response.content) > 1000:
                # 保存图片
                filename = f"{id_number}.jpg"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return filename, None
        except Exception as e:
            continue
    
    return None, f"下载失败: {exercise_id}"

def main():
    # 读取练习数据
    with open("output/ace_fitness/exercises_full.json", "r", encoding="utf-8") as f:
        exercises = json.load(f)
    
    print(f"开始下载 {len(exercises)} 个训练图片...")
    print(f"保存目录: {OUTPUT_DIR}")
    print("=" * 50)
    
    success = 0
    failed = []
    image_map = {}
    
    # 并行下载
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_image, ex): ex for ex in exercises}
        
        for i, future in enumerate(as_completed(futures)):
            exercise = futures[future]
            exercise_id = exercise.get('id', '')
            
            try:
                filename, error = future.result()
                if filename:
                    success += 1
                    image_map[exercise_id] = f"/public/images/conditioning/{filename}"
                    if success % 20 == 0:
                        print(f"  已下载 {success} 张...")
                else:
                    failed.append(exercise_id)
            except Exception as e:
                failed.append(exercise_id)
    
    print(f"\n✅ 下载完成!")
    print(f"   成功: {success}")
    print(f"   失败: {len(failed)}")
    
    if failed and len(failed) <= 20:
        print(f"   失败列表: {failed}")
    
    # 保存图片映射
    with open("output/ace_fitness/image_map.json", "w", encoding="utf-8") as f:
        json.dump(image_map, f, ensure_ascii=False, indent=2)
    
    print(f"\n图片映射已保存到: output/ace_fitness/image_map.json")
    
    return image_map

if __name__ == "__main__":
    main()
