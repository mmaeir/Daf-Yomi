#!/usr/bin/env python3
"""
הורדת פירוש המלבי"ם על ספר תהילים מ-Sefaria API
"""

import requests
import json
import time
import os

def download_malvim_tehillim():
    print("מוריד את פירוש המלבי\"ם על ספר תהילים...")

    # קבל את מבנה הספר תהילים
    response = requests.get('https://www.sefaria.org/api/v2/raw/index/Psalms')
    if not response.ok:
        print("שגיאה בקבלת מבנה הספר")
        return

    data = response.json()
    print(f"יש {len(data.get('schema', {}).get('nodes', []))} פרקים")

    all_commentary = []

    # הורד את הפירוש לכל הפרקים (1-150)
    for i in range(1, 151):
        print(f"מוריד פירוש לפרק {i}...")
        commentary_response = requests.get(f'https://www.sefaria.org/api/texts/Malbim on Psalms.{i}?lang=he&commentary=0&context=0')

        if commentary_response.ok:
            commentary_data = commentary_response.json()
            hebrew_commentary = commentary_data.get('he', [])

            if isinstance(hebrew_commentary, list):
                hebrew_commentary = '\n\n'.join(hebrew_commentary)
            elif isinstance(hebrew_commentary, str):
                pass  # כבר string
            else:
                hebrew_commentary = str(hebrew_commentary)

            if hebrew_commentary.strip():
                all_commentary.append(f"--- פירוש המלבי\"ם על פרק {i} ---\n{hebrew_commentary}")
            else:
                all_commentary.append(f"--- פירוש המלבי\"ם על פרק {i} ---\n[אין פירוש זמין]")
        else:
            print(f"שגיאה בהורדת פירוש לפרק {i}")
            all_commentary.append(f"--- פירוש המלבי\"ם על פרק {i} ---\n[שגיאה בהורדת הפירוש]")

        # המתן קצת כדי לא להעמיס על השרת
        time.sleep(0.5)

    # שמור לקובץ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'malvim_on_tehillim.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n\n'.join(all_commentary))

    print("הקובץ malvim_on_tehillim.txt נשמר בהצלחה!")
    print(f"גודל הקובץ: {len('\n\n\n'.join(all_commentary))} תווים")

if __name__ == "__main__":
    download_malvim_tehillim()




