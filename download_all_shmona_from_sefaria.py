#!/usr/bin/env python3
"""
הורדת כל שמונה הקבצים של הרב קוק מ-Sefaria API ואיחודם לקובץ אחד
"""

import requests
import json
import time
import os

def download_all_shmona_from_sefaria():
    print("מוריד את כל שמונה הקבצים של הרב קוק מ-Sefaria...")
    
    base_path = "Shemonah_Kevatzim"
    all_text = []
    
    # הורד את כל 8 הקבצים
    for kovetz_num in range(1, 9):
        print(f"\nמוריד קובץ {kovetz_num}...")
        kovetz_text = []
        
        # נסה לקבל את מספר הפסקאות בקובץ הזה
        try:
            # נסה לקבל את כל הקובץ בבת אחת
            url = f'https://www.sefaria.org/api/texts/{base_path}.{kovetz_num}?lang=he&commentary=0&context=0'
            response = requests.get(url, timeout=30)
            
            if response.ok:
                data = response.json()
                hebrew_text = data.get('he', [])
                
                if isinstance(hebrew_text, list):
                    # אם זה רשימה של פסקאות, כל פסקה היא רשימה של קטעים
                    for para_idx, paragraph in enumerate(hebrew_text, 1):
                        if isinstance(paragraph, list):
                            para_text = '\n'.join(str(seg) for seg in paragraph if seg)
                        else:
                            para_text = str(paragraph)
                        
                        if para_text.strip():
                            kovetz_text.append(f"פסקה {para_idx}:\n{para_text}")
                    full_text = '\n\n'.join(kovetz_text)
                elif isinstance(hebrew_text, str):
                    full_text = hebrew_text
                else:
                    full_text = str(hebrew_text)
                
                if full_text.strip():
                    all_text.append(f"{'='*60}\nקובץ {kovetz_num}\n{'='*60}\n\n{full_text}")
                    print(f"  קובץ {kovetz_num} הורד בהצלחה ({len(full_text)} תווים)")
                else:
                    print(f"  קובץ {kovetz_num} ריק")
            else:
                print(f"  שגיאה בהורדת קובץ {kovetz_num}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  שגיאה בהורדת קובץ {kovetz_num}: {e}")
        
        # המתן קצת בין הורדות
        time.sleep(0.5)
    
    if not all_text:
        print("\nלא הורד תוכן!")
        return
    
    # שמור לקובץ טקסט אחד
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'shmona_kevatzim_all.txt')
    
    combined_text = '\n\n\n'.join(all_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    print(f"\n{'='*60}")
    print("הקובץ המאוחד נשמר בהצלחה!")
    print(f"שם הקובץ: shmona_kevatzim_all.txt")
    print(f"גודל: {len(combined_text)} תווים ({len(combined_text) / 1024:.2f} KB)")
    print(f"מספר קבצים שהורדו: {len(all_text)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    download_all_shmona_from_sefaria()



