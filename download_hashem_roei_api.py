#!/usr/bin/env python3
"""
הורדת הספר "השם רועי" מאתר ויקיטקסט באמצעות API
"""

import requests
import json
import time
import os
import re
from urllib.parse import quote

def get_wikisource_api_content(title):
    """משוך תוכן מוויקיטקסט באמצעות API"""
    base_url = "https://he.wikisource.org/w/api.php"
    
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': 'main',
        'titles': title,
        'formatversion': '2'
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'he,en-US;q=0.9,en;q=0.8'
        }
        time.sleep(5)  # המתן ארוך מאוד בין בקשות
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 403:
            print(f"  שגיאת rate limiting. ממתין 30 שניות...")
            time.sleep(30)
            # נסה שוב
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        response.raise_for_status()
        data = response.json()
        
        pages = data.get('query', {}).get('pages', [])
        if pages and len(pages) > 0:
            revisions = pages[0].get('revisions', [])
            if revisions and len(revisions) > 0:
                return revisions[0].get('slots', {}).get('main', {}).get('content', '')
        
        return None
    except Exception as e:
        print(f"שגיאה בקבלת {title}: {e}")
        if "403" in str(e) or "rate" in str(e).lower():
            print("  נסה להמתין כמה דקות ולנסות שוב")
        return None

def clean_wikitext(text):
    """נקה טקסט מוויקי markup"""
    if not text:
        return ""
    
    # הסר תבניות ויקי
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    # הסר קישורים
    text = re.sub(r'\[\[([^\|]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    # הסר תגי HTML
    text = re.sub(r'<[^>]+>', '', text)
    # הסר תגי ref
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    # נקה שורות ריקות מרובות
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def find_all_pages(start_title):
    """מצא את כל הדפים של הספר"""
    visited = set()
    pages_to_visit = [start_title]
    all_pages = []
    
    while pages_to_visit:
        current_title = pages_to_visit.pop(0)
        if current_title in visited:
            continue
        
        visited.add(current_title)
        print(f"מוריד: {current_title}")
        
        content = get_wikisource_api_content(current_title)
        if content:
            cleaned = clean_wikitext(content)
            if cleaned:
                all_pages.append((current_title, cleaned))
                print(f"  הורד בהצלחה ({len(cleaned)} תווים)")
            
            # חפש קישורים לדפים נוספים
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in links:
                link_parts = link.split('|')
                link_title = link_parts[0].strip()
                
                # אם זה קישור לדף אחר של הספר
                if 'השם_רועי' in link_title or 'השם רועי' in link_title:
                    if link_title not in visited and link_title not in pages_to_visit:
                        pages_to_visit.append(link_title)
                        print(f"  נמצא קישור נוסף: {link_title}")
        
        time.sleep(5)  # המתן ארוך בין בקשות
    
    return all_pages

def download_book():
    print("מתחיל להוריד את הספר 'השם רועי'...")
    
    # נסה למצוא את דף הספר הראשי
    start_titles = [
        "השם_רועי",
        "השם רועי",
    ]
    
    all_pages = []
    
    for title in start_titles:
        print(f"\nמנסה: {title}")
        pages = find_all_pages(title)
        if pages:
            all_pages = pages
            break
    
    if not all_pages:
        print("לא נמצאו דפים. מנסה דרך דף המחבר...")
        # נסה דרך דף המחבר
        author_content = get_wikisource_api_content("מחבר:אוריאל_ספז")
        if author_content:
            # חפש קישורים לספר
            links = re.findall(r'\[\[([^\]]+)\]\]', author_content)
            for link in links:
                link_parts = link.split('|')
                link_title = link_parts[0].strip()
                if 'רועי' in link_title:
                    print(f"נמצא קישור: {link_title}")
                    pages = find_all_pages(link_title)
                    if pages:
                        all_pages = pages
                        break
    
    if not all_pages:
        print("\nלא נמצאו דפים!")
        return
    
    # מיין לפי שם הדף כדי לשמור על הסדר
    all_pages.sort(key=lambda x: x[0])
    
    # שמור לקובץ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'hashem_roei.txt')
    
    all_text = []
    for i, (title, text) in enumerate(all_pages, 1):
        page_title = title.replace('_', ' ')
        all_text.append(f"{'='*60}\nדף {i}: {page_title}\n{'='*60}\n\n{text}")
    
    combined_text = '\n\n\n'.join(all_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    print(f"\n{'='*60}")
    print("הקובץ נשמר בהצלחה!")
    print(f"שם הקובץ: hashem_roei.txt")
    print(f"גודל: {len(combined_text)} תווים ({len(combined_text) / 1024:.2f} KB)")
    print(f"מספר דפים: {len(all_pages)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    download_book()
