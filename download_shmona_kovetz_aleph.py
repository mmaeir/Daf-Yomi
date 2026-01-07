#!/usr/bin/env python3
"""
הורדת קובץ א' של 'שמונה קבצים' (הרב קוק) כ-PDF מאתר דעת
"""

import requests
import os


def download_kovetz_aleph():
    print("מוריד את קובץ א' של 'שמונה קבצים' (הרב קוק)...")

    url = "https://www.daat.ac.il/daat/vl/shmona/shmona01.pdf"

    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        print("שגיאה בהורדה:", e)
        return

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shmona_kovetz_aleph.pdf")

    try:
        with open(out_path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        print("שגיאה בשמירת הקובץ:", e)
        return

    print("הקובץ נשמר בהצלחה:")
    print(out_path)
    print("גודל:", len(resp.content), "bytes")


if __name__ == "__main__":
    download_kovetz_aleph()




