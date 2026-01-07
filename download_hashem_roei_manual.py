#!/usr/bin/env python3
"""
הורדת הספר "השם רועי" מאתר ויקיטקסט
הערה: בגלל rate limiting של ויקיטקסט, הסקריפט ממתין זמן ארוך בין בקשות
"""

import requests
import json
import time
import os
import re
from urllib.parse import quote

# יצירת session עם cookies
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'he,en-US;q=0.9,en;q=0.8'
})

def get_wikisource_api_content(title, retry_count=0):
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
        # המתן זמן ארוך מאוד בין בקשות (60 שניות)
        if retry_count == 0:
            print(f"  ממתין 60 שניות לפני הבקשה...")
            time.sleep(60)
        else:
            print(f"  ממתין 120 שניות לפני נסיון חוזר...")
            time.sleep(120)
        
        response = session.get(base_url, params=params, timeout=60)
        
        if response.status_code == 403:
            if retry_count < 2:
                print(f"  שגיאת rate limiting. נסיון {retry_count + 1}/3...")
                return get_wikisource_api_content(title, retry_count + 1)
            else:
                print(f"  שגיאת rate limiting - נסה שוב בעוד כמה דקות")
                return None
        
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
        if "403" in str(e) and retry_count < 2:
            return get_wikisource_api_content(title, retry_count + 1)
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
    
    print(f"\nחשוב: בגלל rate limiting, כל דף ייקח כ-60 שניות להורדה")
    print(f"אם יש הרבה דפים, זה עלול לקחת זמן רב...\n")
    
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
                print(f"  ✓ הורד בהצלחה ({len(cleaned)} תווים)")
            
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
        else:
            print(f"  ✗ לא הצלחתי להוריד את הדף")
    
    return all_pages

def download_book():
    print("="*60)
    print("הורדת הספר 'השם רועי' מאתר ויקיטקסט")
    print("="*60)
    print("\nהערה: בגלל rate limiting של ויקיטקסט,")
    print("כל דף ייקח כ-60 שניות להורדה.")
    print("אם יש בעיות, נסה שוב בעוד כמה דקות.\n")
    
    # נסה למצוא את דף הספר הראשי
    start_titles = [
        "השם_רועי",
    ]
    
    all_pages = []
    
    for title in start_titles:
        print(f"מנסה: {title}")
        pages = find_all_pages(title)
        if pages:
            all_pages = pages
            break
    
    if not all_pages:
        print("\nלא נמצאו דפים. נסה שוב בעוד כמה דקות.")
        print("או בדוק ידנית את הקישור: https://he.wikisource.org/wiki/השם_רועי")
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


