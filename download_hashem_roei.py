#!/usr/bin/env python3
"""
הורדת הספר "השם רועי" מאתר ויקיטקסט
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time

def get_wikisource_content(url):
    """משוך תוכן מוויקיטקסט"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'he,en-US;q=0.9,en;q=0.8'
        }
        # המתן לפני כל בקשה
        time.sleep(2)
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"שגיאה בקבלת {url}: {e}")
        return None

def extract_text_from_wikisource(html_content):
    """חלץ טקסט מתוכן HTML של ויקיטקסט"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # מצא את התוכן הראשי
    content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
    
    if not content_div:
        return None
    
    # הסר אלמנטים לא רצויים
    for element in content_div.find_all(['script', 'style', 'nav', 'table', 'div', 'span']):
        if element.get('class') and any(cls in ['navbox', 'toc', 'mw-editsection'] for cls in element.get('class', [])):
            element.decompose()
    
    # חלץ טקסט
    text = content_div.get_text(separator='\n', strip=True)
    
    # נקה טקסט
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line and len(line) > 2:  # התעלם משורות קצרות מדי
            lines.append(line)
    
    return '\n'.join(lines)

def find_book_pages(base_url, book_name):
    """מצא את כל הדפים של הספר"""
    # נסה למצוא את דף הספר
    book_urls = []
    
    # נסה מספר אפשרויות של URL
    possible_urls = [
        f"{base_url}/השם_רועי",
        f"{base_url}/השם רועי",
        f"https://he.wikisource.org/wiki/השם_רועי",
        f"https://he.wikisource.org/wiki/השם רועי",
    ]
    
    # נסה גם דרך דף המחבר
    author_page = get_wikisource_content("https://he.wikisource.org/wiki/מחבר:אוריאל_ספז")
    if author_page:
        soup = BeautifulSoup(author_page, 'html.parser')
        # חפש קישורים לספר
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            text = link.get_text()
            if 'רועי' in text or 'השם רועי' in text:
                full_url = f"https://he.wikisource.org{href}" if href.startswith('/') else href
                book_urls.append(full_url)
                print(f"נמצא קישור: {text} -> {full_url}")
    
    return book_urls

def find_all_book_pages(start_url):
    """מצא את כל הדפים של הספר החל מדף ראשי"""
    visited = set()
    pages_to_visit = [start_url]
    all_pages = []
    
    while pages_to_visit:
        current_url = pages_to_visit.pop(0)
        if current_url in visited:
            continue
        
        visited.add(current_url)
        print(f"בודק: {current_url}")
        
        content = get_wikisource_content(current_url)
        if not content:
            continue
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # חלץ את התוכן של הדף הנוכחי
        text = extract_text_from_wikisource(content)
        if text:
            all_pages.append((current_url, text))
            print(f"  נמצא תוכן ({len(text)} תווים)")
        
        # חפש קישורים לדפים נוספים של הספר
        content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
        if content_div:
            links = content_div.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                link_text = link.get_text().strip()
                
                # אם זה קישור לדף אחר של הספר
                if href.startswith('/wiki/') and 'השם_רועי' in href:
                    full_url = f"https://he.wikisource.org{href}"
                    if full_url not in visited and full_url not in pages_to_visit:
                        pages_to_visit.append(full_url)
                        print(f"  נמצא קישור נוסף: {link_text} -> {full_url}")
        
        time.sleep(2)  # המתן בין בקשות (כדי לא להעמיס על השרת)
    
    return all_pages

def download_book():
    print("מתחיל להוריד את הספר 'השם רועי'...")
    
    # נסה למצוא את דף הספר הראשי
    base_urls = [
        "https://he.wikisource.org/wiki/השם_רועי",
        "https://he.wikisource.org/wiki/השם רועי",
    ]
    
    # גם נסה דרך דף המחבר
    author_url = "https://he.wikisource.org/wiki/מחבר:אוריאל_ספז"
    print(f"בודק דף המחבר: {author_url}")
    
    author_content = get_wikisource_content(author_url)
    start_url = None
    
    if author_content:
        soup = BeautifulSoup(author_content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            link_text = link.get_text().strip()
            href = link.get('href', '')
            if 'רועי' in link_text or 'השם רועי' in link_text:
                if href.startswith('/wiki/'):
                    start_url = f"https://he.wikisource.org{href}"
                    print(f"נמצא קישור לספר: {link_text} -> {start_url}")
                    break
    
    if not start_url:
        # נסה את ה-URL-ים הישירים
        for url in base_urls:
            print(f"מנסה URL ישיר: {url}")
            content = get_wikisource_content(url)
            if content:
                start_url = url
                break
    
    if not start_url:
        print("לא הצלחתי למצוא את דף הספר")
        return
    
    print(f"\nמתחיל להוריד מהדף: {start_url}")
    
    # מצא את כל הדפים
    all_pages = find_all_book_pages(start_url)
    
    if not all_pages:
        print("לא נמצאו דפים")
        return
    
    # מיין לפי URL כדי לשמור על הסדר
    all_pages.sort(key=lambda x: x[0])
    
    all_text = []
    for i, (url, text) in enumerate(all_pages, 1):
        page_title = url.split('/')[-1].replace('_', ' ')
        all_text.append(f"{'='*60}\nדף {i}: {page_title}\n{'='*60}\n\n{text}")
    
    if not all_text:
        print("\nלא הורד תוכן!")
        return
    
    # שמור לקובץ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'hashem_roei.txt')
    
    combined_text = '\n\n\n'.join(all_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    print(f"\n{'='*60}")
    print("הקובץ נשמר בהצלחה!")
    print(f"שם הקובץ: hashem_roei.txt")
    print(f"גודל: {len(combined_text)} תווים ({len(combined_text) / 1024:.2f} KB)")
    print(f"{'='*60}")

if __name__ == "__main__":
    download_book()
