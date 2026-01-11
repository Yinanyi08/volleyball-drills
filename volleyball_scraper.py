#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VolleyballXpert.com 训练内容抓取器 (v3 - 高速并发版)
使用线程池并发抓取，大幅提升速度
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 基础配置
BASE_URL = "https://volleyballxpert.com"
OUTPUT_DIR = Path(__file__).parent / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
AGE_DIR = OUTPUT_DIR / "drills_by_age"

# 并发配置
MAX_WORKERS = 10  # 并发线程数
REQUEST_TIMEOUT = 30

# 年龄段分类
AGE_CATEGORIES = {
    "beginner": {"url": f"{BASE_URL}/drills/age/beginner", "name_cn": "初级 (6-10岁)"},
    "intermediate": {"url": f"{BASE_URL}/drills/age/intermediate", "name_cn": "中级 (10-14岁)"},
    "high_school": {"url": f"{BASE_URL}/drills/age/high-school", "name_cn": "高中 (14-18岁)"},
    "advanced": {"url": f"{BASE_URL}/drills/age/advanced", "name_cn": "高级 (18岁+)"}
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# 线程安全计数器
lock = threading.Lock()
progress = {"done": 0, "total": 0}


def create_session():
    """创建带重试的Session"""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session


def create_directories():
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    AGE_DIR.mkdir(exist_ok=True)


def fetch_page(session, url):
    """获取网页"""
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.content, 'html.parser')
    except:
        return None


def get_all_drill_links(session):
    """从所有分类页面获取全部训练链接"""
    all_links = {}  # {url: [categories]}
    
    for cat_key, cat_info in AGE_CATEGORIES.items():
        soup = fetch_page(session, cat_info['url'])
        if not soup:
            continue
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/drills/details/' in href:
                full_url = urljoin(BASE_URL, href)
                if full_url not in all_links:
                    all_links[full_url] = []
                all_links[full_url].append(cat_key)
    
    return all_links


def parse_drill(session, url, categories):
    """解析单个训练详情"""
    global progress
    
    soup = fetch_page(session, url)
    if not soup:
        return None
    
    slug = url.split('/')[-1]
    
    drill = {
        "url": url,
        "slug": slug,
        "title": "",
        "description": "",
        "setup": {"players": "", "court": "", "equipment": "", "roles": ""},
        "steps": [],
        "variations": [],
        "coaching_tips": [],
        "image_url": "",
        "local_image": "",
        "age_groups": categories
    }
    
    # 标题和描述
    h1 = soup.find('h1')
    if h1:
        drill["title"] = h1.get_text(strip=True)
    h2 = soup.find('h2')
    if h2:
        drill["description"] = h2.get_text(strip=True)
    
    # 设置信息
    page_text = soup.get_text()
    for key, pattern in [
        ("players", r"Players?:\s*(.+?)(?:\n|$)"),
        ("court", r"Court:\s*(.+?)(?:\n|$)"),
        ("equipment", r"Equipment:\s*(.+?)(?:\n|$)"),
        ("roles", r"Roles?:\s*(.+?)(?:\n|$)")
    ]:
        m = re.search(pattern, page_text, re.IGNORECASE)
        if m:
            drill["setup"][key] = m.group(1).strip()
    
    # 列表项
    steps, variations, tips = [], [], []
    for li in soup.find_all('li'):
        text = li.get_text(strip=True)
        if not text or len(text) < 10:
            continue
        tl = text.lower()
        if any(x in tl for x in ['drills', 'volleyball', 'age', 'home']) and len(text) < 50:
            continue
        if re.match(r'^\d+\.?\s', text):
            steps.append(text)
        elif any(x in tl for x in ['variation', 'instead', 'add', 'increase']):
            variations.append(text)
        elif any(x in tl for x in ['emphasis', 'focus', 'technique', 'position']):
            tips.append(text)
        elif len(text) > 50:
            steps.append(text)
    
    drill["steps"] = steps[:10]
    drill["variations"] = variations[:5]
    drill["coaching_tips"] = tips[:5]
    
    # 图片
    for img in soup.find_all('img', src=True):
        src = img['src']
        if '/drills/' in src and '.png' in src.lower():
            drill["image_url"] = urljoin(BASE_URL, src)
            # 下载图片
            try:
                img_resp = session.get(drill["image_url"], timeout=REQUEST_TIMEOUT)
                if img_resp.ok:
                    filepath = IMAGES_DIR / f"{slug}.png"
                    with open(filepath, 'wb') as f:
                        f.write(img_resp.content)
                    drill["local_image"] = f"images/{slug}.png"
            except:
                pass
            break
    
    with lock:
        progress["done"] += 1
        print(f"\r  进度: {progress['done']}/{progress['total']} ({100*progress['done']//progress['total']}%)", end="", flush=True)
    
    return drill


def main():
    print("=" * 60)
    print("VolleyballXpert.com 排球训练抓取器 (v3 并发版)")
    print("=" * 60)
    
    create_directories()
    session = create_session()
    
    # 1. 获取所有训练链接
    print("\n[1/3] 获取所有训练链接...")
    all_links = get_all_drill_links(session)
    print(f"✓ 发现 {len(all_links)} 个不重复训练")
    
    progress["total"] = len(all_links)
    progress["done"] = 0
    
    # 2. 并发抓取所有训练详情
    print(f"\n[2/3] 并发抓取训练详情 ({MAX_WORKERS} 线程)...")
    all_drills = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(parse_drill, session, url, cats): url 
            for url, cats in all_links.items()
        }
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                all_drills.append(result)
    
    print(f"\n✓ 成功抓取 {len(all_drills)} 个训练")
    
    # 3. 保存结果
    print("\n[3/3] 保存数据...")
    
    # 总数据
    with open(OUTPUT_DIR / "drills_data.json", 'w', encoding='utf-8') as f:
        json.dump(all_drills, f, ensure_ascii=False, indent=2)
    
    # 按年龄段分类
    by_age = {k: [] for k in AGE_CATEGORIES}
    for drill in all_drills:
        for age in drill["age_groups"]:
            by_age[age].append(drill)
    
    for age_key, drills in by_age.items():
        with open(AGE_DIR / f"{age_key}.json", 'w', encoding='utf-8') as f:
            json.dump(drills, f, ensure_ascii=False, indent=2)
    
    # 摘要
    summary = {
        "total_drills": len(all_drills),
        "by_category": {k: len(v) for k, v in by_age.items()},
        "images_downloaded": sum(1 for d in all_drills if d.get("local_image")),
        "scrape_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(OUTPUT_DIR / "summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("抓取完成!")
    print("=" * 60)
    print(f"• 总训练数: {summary['total_drills']}")
    print(f"• 图片数: {summary['images_downloaded']}")
    for cat, count in summary['by_category'].items():
        print(f"  - {AGE_CATEGORIES[cat]['name_cn']}: {count}")
    print(f"\n输出: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
