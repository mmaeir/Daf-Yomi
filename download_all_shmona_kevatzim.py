#!/usr/bin/env python3
"""
הורדת כל שמונה הקבצים של הרב קוק ואיחודם לקובץ אחד
"""

import requests
import os
import time

def download_all_shmona_kevatzim():
    print("מוריד את כל שמונה הקבצים של הרב קוק...")
    
    # נסה מספר URL-ים אפשריים
    base_urls = [
        "https://www.daat.ac.il/daat/vl/shmona/shmona{:02d}.pdf",
        "https://www.daat.ac.il/daat/vl/shmona/shmona{:d}.pdf",
        "https://www.daat.ac.il/daat/vl/shmona/kovetz{:d}.pdf",
    ]
    all_pdfs = []
    
    # הורד את כל 8 הקבצים
    for i in range(1, 9):
        print(f"מוריד קובץ {i}...")
        downloaded = False
        
        # נסה מספר URL-ים אפשריים
        for base_url_template in base_urls:
            try:
                url = base_url_template.format(i)
                response = requests.get(url, timeout=60)
                if response.ok and len(response.content) > 1000:  # ודא שזה לא דף שגיאה
                    all_pdfs.append({
                        'number': i,
                        'content': response.content,
                        'size': len(response.content)
                    })
                    print(f"  קובץ {i} הורד בהצלחה מ-{url} ({len(response.content)} bytes)")
                    downloaded = True
                    break
            except Exception as e:
                continue
        
        if not downloaded:
            print(f"  לא נמצא קובץ {i} באף אחד מהמקורות")
            all_pdfs.append({
                'number': i,
                'content': None,
                'size': 0
            })
        
        # המתן קצת בין הורדות
        time.sleep(0.5)
    
    if not all_pdfs:
        print("לא הורדו קבצים!")
        return
    
    # שמור כל קובץ בנפרד
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\nשומר קבצים נפרדים...")
    for pdf_data in all_pdfs:
        if pdf_data['content']:
            filename = f"shmona_kovetz_{pdf_data['number']}.pdf"
            file_path = os.path.join(current_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(pdf_data['content'])
            print(f"  נשמר: {filename}")
    
    # אגד את כל הקבצים לקובץ PDF אחד
    print("\nמאחד את כל הקבצים לקובץ אחד...")
    
    try:
        # נסה להשתמש ב-PyPDF2 או pypdf לאיחוד הקבצים
        try:
            from PyPDF2 import PdfMerger
            merger = PdfMerger()
            
            for pdf_data in all_pdfs:
                if pdf_data['content']:
                    import io
                    pdf_file = io.BytesIO(pdf_data['content'])
                    merger.append(pdf_file)
            
            merged_path = os.path.join(current_dir, 'shmona_kevatzim_all.pdf')
            with open(merged_path, 'wb') as output_file:
                merger.write(output_file)
            
            print(f"הקובץ המאוחד נשמר: shmona_kevatzim_all.pdf")
            print(f"גודל: {os.path.getsize(merged_path)} bytes")
            
        except ImportError:
            # אם PyPDF2 לא מותקן, פשוט שמור את כל הקבצים כקובץ בינארי אחד
            print("PyPDF2 לא מותקן. מאחד את הקבצים כקובץ בינארי...")
            merged_path = os.path.join(current_dir, 'shmona_kevatzim_all.bin')
            with open(merged_path, 'wb') as output_file:
                for pdf_data in all_pdfs:
                    if pdf_data['content']:
                        # כתוב מספר הקובץ
                        output_file.write(f"=== KOVETZ {pdf_data['number']} ===\n".encode('utf-8'))
                        output_file.write(pdf_data['content'])
                        output_file.write(b"\n\n")
            
            print(f"הקובץ המאוחד נשמר: shmona_kevatzim_all.bin")
            print(f"גודל: {os.path.getsize(merged_path)} bytes")
            print("הערה: זהו קובץ בינארי. להתקנת PyPDF2 להמרה ל-PDF: pip install PyPDF2")
            
    except Exception as e:
        print(f"שגיאה באיחוד הקבצים: {e}")
        print("הקבצים נשמרו בנפרד.")
    
    print("\nסיכום:")
    total_size = sum(pdf['size'] for pdf in all_pdfs if pdf['content'])
    print(f"סה\"כ הורדו: {len([p for p in all_pdfs if p['content']])} קבצים")
    print(f"גודל כולל: {total_size} bytes ({total_size / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    download_all_shmona_kevatzim()
