#!/usr/bin/env python3
"""
הורדת שמונה קבצים מ-Sefaria API
"""

import requests
import json
import time
import os

def download_from_sefaria():
    print("בודק זמינות ב-Sefaria API...")
    
    # נסה למצוא את המבנה ב-Sefaria
    try:
        response = requests.get('https://www.sefaria.org/api/v2/raw/index/Shemonah_Kevatzim')
        if response.ok:
            data = response.json()
            print("נמצא ב-Sefaria!")
            print("מבנה:", json.dumps(data, indent=2, ensure_ascii=False)[:500])
        else:
            print("לא נמצא ב-Sefaria")
    except Exception as e:
        print(f"שגיאה: {e}")
    
    # נסה גם גרסאות אחרות של השם
    variations = [
        'Shemonah_Kevatzim',
        'Shemonah Kevatzim',
        'Shmonah_Kevatzim',
        'Shmonah Kevatzim',
    ]
    
    for var in variations:
        try:
            url = f'https://www.sefaria.org/api/v2/raw/index/{var}'
            response = requests.get(url, timeout=10)
            if response.ok:
                print(f"נמצא: {var}")
                data = response.json()
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        except:
            pass

if __name__ == "__main__":
    download_from_sefaria()


