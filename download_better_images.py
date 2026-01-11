import json
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
DRILLS_DIR = "public/images/drills"
COND_DIR = "public/images/conditioning"
os.makedirs(DRILLS_DIR, exist_ok=True)
os.makedirs(COND_DIR, exist_ok=True)

def download_file(url, target_path):
    try:
        # User-agent to avoid blocking
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200 and len(response.content) > 2000:
            with open(target_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        pass
    return False

def download_drills():
    print("Downloading better images for drills...")
    with open("output/drills_data.json", "r", encoding="utf-8") as f:
        drills = json.load(f)
    
    success = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for d in drills:
            url = d.get('image_url', '')
            if '350x250' in url:
                # https://volleyballxpert.com/images/volleyball/drills/350x250/99.png -> https://volleyballxpert.com/images/volleyball/drills/99.png
                high_res_url = url.replace('350x250/', '')
                slug = d.get('slug')
                target = os.path.join(DRILLS_DIR, f"{slug}.png")
                futures.append(executor.submit(download_file, high_res_url, target))
        
        for f in as_completed(futures):
            if f.result(): success += 1
    print(f"Drills: Downloaded {success} better images.")

def download_conditioning():
    print("Downloading high-res images for conditioning...")
    with open("output/ace_fitness/exercises_full.json", "r", encoding="utf-8") as f:
        exercises = json.load(f)
    
    success = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for ex in exercises:
            exercise_id = ex.get('id', '')
            match = re.match(r'^(\d+)-', exercise_id)
            if match:
                id_num = match.group(1)
                for suffix in ['2', '1', '3']:
                    # Use ?tr=w-1000 for high resolution via ImageKit
                    url = f"https://ik.imagekit.io/02fmeo4exvw/exercise-library/large/{id_num}-{suffix}.jpg?tr=w-1000"
                    target = os.path.join(COND_DIR, f"{id_num}.jpg")
                    futures.append(executor.submit(download_file, url, target))
                    break # Usually suffix 2 is best, we only need one success per ID
        
        for f in as_completed(futures):
            if f.result(): success += 1
    print(f"Conditioning: Downloaded {success} high-res images.")

if __name__ == "__main__":
    download_drills()
    download_conditioning()
