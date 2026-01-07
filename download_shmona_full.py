#!/usr/bin/env python3
"""
הורדת כל שמונה הקבצים של הרב קוק מ-Sefaria API עם כל הפסקאות המלאות
"""

import requests
import json
import time
import os

def download_shmona_full():
    print("מוריד את כל שמונה הקבצים של הרב קוק מ-Sefaria...")
    
    base_path = "Shemonah_Kevatzim"
    all_text = []
    
    # הורד את כל 8 הקבצים
    for kovetz_num in range(1, 9):
        print(f"\nמוריד קובץ {kovetz_num}...")
        kovetz_text = []
        
        try:
            # הורד את כל הקובץ בבת אחת
            url = f'https://www.sefaria.org/api/texts/{base_path}.{kovetz_num}?lang=he&commentary=0&context=0'
            response = requests.get(url, timeout=60)
            
            if response.ok:
                data = response.json()
                hebrew_text = data.get('he', [])
                
                if isinstance(hebrew_text, list):
                    # כל קובץ מכיל רשימה של פסקאות
                    for para_idx, paragraph in enumerate(hebrew_text, 1):
                        if paragraph is None:
                            continue
                            
                        if isinstance(paragraph, list):
                            # כל פסקה היא רשימה של קטעים
                            para_segments = []
                            for seg in paragraph:
                                if seg:
                                    para_segments.append(str(seg).strip())
                            para_text = '\n'.join(para_segments)
                        elif isinstance(paragraph, str):
                            para_text = paragraph.strip()
                        else:
                            para_text = str(paragraph).strip()
                        
                        if para_text:
                            kovetz_text.append(para_text)
                    
                    if kovetz_text:
                        full_text = '\n\n'.join(kovetz_text)
                        all_text.append(f"{'='*60}\nקובץ {kovetz_num}\n{'='*60}\n\n{full_text}")
                        print(f"  קובץ {kovetz_num} הורד בהצלחה ({len(full_text)} תווים, {len(kovetz_text)} פסקאות)")
                    else:
                        print(f"  קובץ {kovetz_num} ריק")
                else:
                    print(f"  קובץ {kovetz_num}: מבנה לא צפוי - {type(hebrew_text)}")
                    
        except Exception as e:
            print(f"  שגיאה בהורדת קובץ {kovetz_num}: {e}")
            import traceback
            traceback.print_exc()
        
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
    download_shmona_full()



