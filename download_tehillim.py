#!/usr/bin/env python3
"""
הורדת כל ספר תהילים מ-Sefaria API
"""

import requests
import json
import time

def download_tehillim():
    print("מוריד את ספר תהילים...")

    # קבל את מבנה הספר תהילים
    response = requests.get('https://www.sefaria.org/api/v2/raw/index/Psalms')
    if not response.ok:
        print("שגיאה בקבלת מבנה הספר")
        return

    data = response.json()
    print(f"יש {len(data.get('schema', {}).get('nodes', []))} פרקים")

    all_text = []

    # הורד את כל הפרקים (1-150)
    for i in range(1, 151):
        print(f"מוריד פרק {i}...")
        text_response = requests.get(f'https://www.sefaria.org/api/texts/Psalms.{i}?lang=he&commentary=0&context=0')

        if text_response.ok:
            text_data = text_response.json()
            hebrew_text = text_data.get('he', [])

            if isinstance(hebrew_text, list):
                hebrew_text = '\n\n'.join(hebrew_text)
            elif isinstance(hebrew_text, str):
                pass  # כבר string
            else:
                hebrew_text = str(hebrew_text)

            all_text.append(f"--- פרק {i} ---\n{hebrew_text}")
        else:
            print(f"שגיאה בהורדת פרק {i}")
            all_text.append(f"--- פרק {i} ---\n[שגיאה בהורדת הפרק]")

        # המתן קצת כדי לא להעמיס על השרת
        time.sleep(0.5)

    # שמור לקובץ
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'tehillim_full.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n\n'.join(all_text))

    print("הקובץ tehillim_full.txt נשמר בהצלחה!")
    print(f"גודל הקובץ: {len('\n\n\n'.join(all_text))} תווים")

if __name__ == "__main__":
    download_tehillim()
