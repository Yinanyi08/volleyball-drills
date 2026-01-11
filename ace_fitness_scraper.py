"""
ACE Fitness Complete Scraper - 完整版
爬取 ACE Fitness 网站全部 330 个训练动作
使用分页和多入口策略
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.acefitness.org"
OUTPUT_DIR = "output/ace_fitness"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_links_with_pagination(base_url, max_pages=15):
    """获取分页页面的所有链接"""
    all_links = set()
    
    for page in range(1, max_pages + 1):
        # ACE 网站的分页格式
        url = f"{base_url}" if page == 1 else f"{base_url}?page={page}"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找训练链接
            found = 0
            for link in soup.find_all('a', href=True):
                href = link['href']
                match = re.search(r'/exercise-library/(\d+)/', href)
                if match:
                    full_url = href if href.startswith('http') else BASE_URL + href
                    if full_url not in all_links:
                        all_links.add(full_url)
                        found += 1
            
            if found == 0:
                break  # 没有更多内容
                
            time.sleep(0.3)
            
        except Exception as e:
            print(f"    Error: {e}")
            break
    
    return all_links

def get_all_exercise_links():
    """获取所有训练链接"""
    all_links = set()
    
    # 主要入口：按难度级别（这是最可靠的分类）
    experience_urls = [
        f"{BASE_URL}/resources/everyone/exercise-library/experience/beginner/",
        f"{BASE_URL}/resources/everyone/exercise-library/experience/intermediate/",
        f"{BASE_URL}/resources/everyone/exercise-library/experience/advanced/"
    ]
    
    print("[Step 1] 从难度分类页面收集链接...")
    for url in experience_urls:
        level = url.split('/')[-2]
        print(f"  正在爬取: {level}")
        links = get_links_with_pagination(url)
        print(f"    找到 {len(links)} 个链接")
        all_links.update(links)
        time.sleep(0.5)
    
    # 备用入口：主页面（无筛选）
    main_url = f"{BASE_URL}/resources/everyone/exercise-library/"
    print(f"\n  正在爬取: 主页面")
    links = get_links_with_pagination(main_url)
    print(f"    找到 {len(links)} 个链接")
    all_links.update(links)
    
    print(f"\n总计找到 {len(all_links)} 个唯一训练链接")
    return list(all_links)

def parse_exercise_page(url):
    """解析单个训练页面"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()
        
        # 提取ID
        match = re.search(r'/exercise-library/(\d+)/([^/]+)/', url)
        exercise_id = f"{match.group(1)}-{match.group(2)}" if match else url.split('/')[-2]
        
        # 提取标题
        title = ""
        title_elem = soup.find('h1')
        if title_elem:
            title = title_elem.get_text(strip=True)
        
        # 提取难度
        difficulty = ""
        if 'Beginner' in page_text:
            difficulty = 'Beginner'
        elif 'Intermediate' in page_text:
            difficulty = 'Intermediate'
        elif 'Advanced' in page_text:
            difficulty = 'Advanced'
        
        # 提取器材
        equipment = "No Equipment"
        eq_match = re.search(r'Equipment[:\s]+([A-Za-z,/\s-]+?)(?:Difficulty|Target|$)', page_text)
        if eq_match:
            equipment = eq_match.group(1).strip()
            equipment = re.sub(r'\s+', ' ', equipment)
        
        # 提取目标部位
        target = ""
        target_match = re.search(r'Target Body Part[:\s]+([A-Za-z,/\s-]+?)(?:Equipment|Difficulty|$)', page_text)
        if target_match:
            target = target_match.group(1).strip()
        
        # 提取步骤
        steps = []
        content = soup.find('article') or soup.find('main') or soup
        for p in content.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 40 and not any(skip in text.lower() for skip in [
                'share', 'print', 'related', 'subscribe', 'copyright',
                'create fitness', 'practicing equity', 'special olympics'
            ]):
                steps.append(text)
        
        return {
            'id': exercise_id,
            'url': url,
            'title': title,
            'difficulty': difficulty,
            'equipment': equipment[:100] if equipment else "No Equipment",
            'targetBodyPart': target[:100] if target else "",
            'steps': steps[:5]
        }
        
    except Exception as e:
        return None

def scrape_all():
    """主函数"""
    print("=" * 60)
    print("ACE Fitness Complete Scraper v2")
    print("目标: 爬取全部 330 个训练动作")
    print("=" * 60)
    
    # Step 1: 收集链接
    all_links = get_all_exercise_links()
    
    # 保存链接
    with open(f"{OUTPUT_DIR}/all_links_v2.json", 'w', encoding='utf-8') as f:
        json.dump(all_links, f, indent=2)
    
    # Step 2: 并行解析页面
    print(f"\n[Step 2] 解析 {len(all_links)} 个训练页面...")
    all_exercises = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(parse_exercise_page, url): url for url in all_links}
        
        for i, future in enumerate(as_completed(futures)):
            url = futures[future]
            try:
                result = future.result()
                if result and result.get('title') and result.get('steps'):
                    all_exercises.append(result)
                    if (i + 1) % 20 == 0:
                        print(f"  已处理 {i+1}/{len(all_links)}，有效数据 {len(all_exercises)} 条")
            except Exception as e:
                pass
    
    # Step 3: 保存结果
    with open(f"{OUTPUT_DIR}/exercises_full.json", 'w', encoding='utf-8') as f:
        json.dump(all_exercises, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 爬取完成!")
    print(f"   总链接数: {len(all_links)}")
    print(f"   有效数据: {len(all_exercises)}")
    
    # 统计
    difficulties = {}
    for ex in all_exercises:
        d = ex.get('difficulty', 'Unknown')
        difficulties[d] = difficulties.get(d, 0) + 1
    
    print(f"\n难度统计:")
    for d, count in sorted(difficulties.items()):
        print(f"   {d}: {count}")
    
    return all_exercises

if __name__ == "__main__":
    scrape_all()
