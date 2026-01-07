#!/usr/bin/env python3
"""
הורדת כל שמונה הקבצים של הרב קוק מ-Sefaria API עם כל הפסקאות
"""

import requests
import json
import time
import os

def download_all_shmona_complete():
    print("מוריד את כל שמונה הקבצים של הרב קוק מ-Sefaria...")
    
    base_path = "Shemonah_Kevatzim"
    all_text = []
    
    # מספר הפסקאות בכל קובץ (לפי המבנה ב-Sefaria)
    # נבדוק את המבנה תחילה
    try:
        index_response = requests.get(f'https://www.sefaria.org/api/v2/raw/index/{base_path}')
        if index_response.ok:
            index_data = index_response.json()
            lengths = index_data.get('schema', {}).get('lengths', [])
            if len(lengths) >= 2:
                total_paragraphs = lengths[1]  # מספר הפסקאות הכולל
                print(f"נמצאו {total_paragraphs} פסקאות בסך הכל")
    except:
        pass
    
    # הורד את כל 8 הקבצים
    for kovetz_num in range(1, 9):
        print(f"\nמוריד קובץ {kovetz_num}...")
        kovetz_text = []
        
        # נסה להוריד את כל הקובץ
        try:
            url = f'https://www.sefaria.org/api/texts/{base_path}.{kovetz_num}?lang=he&commentary=0&context=0'
            response = requests.get(url, timeout=30)
            
            if response.ok:
                data = response.json()
                hebrew_text = data.get('he', [])
                
                if isinstance(hebrew_text, list) and len(hebrew_text) > 0:
                    # אם זה רשימה של פסקאות
                    for para_idx, paragraph in enumerate(hebrew_text, 1):
                        if isinstance(paragraph, list):
                            # כל פסקה היא רשימה של קטעים
                            para_text = '\n'.join(str(seg).strip() for seg in paragraph if seg and str(seg).strip())
                        elif paragraph:
                            para_text = str(paragraph).strip()
                        else:
                            continue
                        
                        if para_text:
                            kovetz_text.append(f"פסקה {para_idx}:\n{para_text}")
                    
                    full_text = '\n\n'.join(kovetz_text)
                    
                    if full_text.strip():
                        all_text.append(f"{'='*60}\nקובץ {kovetz_num}\n{'='*60}\n\n{full_text}")
                        print(f"  קובץ {kovetz_num} הורד בהצלחה ({len(full_text)} תווים, {len(kovetz_text)} פסקאות)")
                    else:
                        print(f"  קובץ {kovetz_num} ריק")
                else:
                    print(f"  קובץ {kovetz_num}: מבנה לא צפוי")
                    
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
    download_all_shmona_complete()



