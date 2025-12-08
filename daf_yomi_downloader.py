#!/usr/bin/env python3
"""
Automated Daf Yomi Downloader
Downloads Hebrew Talmud texts and Steinsaltz commentary from Sefaria.org API
"""

import requests
import os
import sys
import time
from typing import List, Optional, Tuple
import argparse

# Tractate data from the original app
TRACTATES = [
    {"english": "Berakhot", "hebrew": "ברכות", "daf_count": 64},
    {"english": "Shabbat", "hebrew": "שבת", "daf_count": 157},
    {"english": "Eruvin", "hebrew": "עירובין", "daf_count": 105},
    {"english": "Pesachim", "hebrew": "פסחים", "daf_count": 121},
    {"english": "Shekalim", "hebrew": "שקלים", "daf_count": 22},
    {"english": "Yoma", "hebrew": "יומא", "daf_count": 88},
    {"english": "Sukkah", "hebrew": "סוכה", "daf_count": 56},
    {"english": "Beitzah", "hebrew": "ביצה", "daf_count": 40},
    {"english": "Rosh Hashanah", "hebrew": "ראש השנה", "daf_count": 35},
    {"english": "Taanit", "hebrew": "תענית", "daf_count": 31},
    {"english": "Megillah", "hebrew": "מגילה", "daf_count": 32},
    {"english": "Moed Katan", "hebrew": "מועד קטן", "daf_count": 29},
    {"english": "Chagigah", "hebrew": "חגיגה", "daf_count": 27},
    {"english": "Yevamot", "hebrew": "יבמות", "daf_count": 122},
    {"english": "Ketubot", "hebrew": "כתובות", "daf_count": 112},
    {"english": "Nedarim", "hebrew": "נדרים", "daf_count": 91},
    {"english": "Nazir", "hebrew": "נזיר", "daf_count": 66},
    {"english": "Sotah", "hebrew": "סוטה", "daf_count": 49},
    {"english": "Gittin", "hebrew": "גיטין", "daf_count": 90},
    {"english": "Kiddushin", "hebrew": "קידושין", "daf_count": 82},
    {"english": "Bava Kamma", "hebrew": "בבא קמא", "daf_count": 119},
    {"english": "Bava Metzia", "hebrew": "בבא מציעא", "daf_count": 119},
    {"english": "Bava Batra", "hebrew": "בבא בתרא", "daf_count": 175},
    {"english": "Sanhedrin", "hebrew": "סנהדרין", "daf_count": 113},
    {"english": "Makkot", "hebrew": "מכות", "daf_count": 24},
    {"english": "Shevuot", "hebrew": "שבועות", "daf_count": 49},
    {"english": "Avodah Zarah", "hebrew": "עבודה זרה", "daf_count": 76},
    {"english": "Horayot", "hebrew": "הוריות", "daf_count": 14},
    {"english": "Zevachim", "hebrew": "זבחים", "daf_count": 120},
    {"english": "Menachot", "hebrew": "מנחות", "daf_count": 110},
    {"english": "Chullin", "hebrew": "חולין", "daf_count": 142},
    {"english": "Bechorot", "hebrew": "בכורות", "daf_count": 61},
    {"english": "Arachin", "hebrew": "ערכין", "daf_count": 34},
    {"english": "Temurah", "hebrew": "תמורה", "daf_count": 34},
    {"english": "Keritot", "hebrew": "כריתות", "daf_count": 28},
    {"english": "Meilah", "hebrew": "מעילה", "daf_count": 22},
    {"english": "Kinnim", "hebrew": "קינים", "daf_count": 4},
    {"english": "Tamid", "hebrew": "תמיד", "daf_count": 10},
    {"english": "Middot", "hebrew": "מידות", "daf_count": 4},
    {"english": "Niddah", "hebrew": "נדה", "daf_count": 73}
]

class DafYomiDownloader:
    def __init__(self, output_dir: str = "downloads", delay: float = 1.0):
        """
        Initialize the downloader.
        
        Args:
            output_dir: Directory to save downloaded files
            delay: Delay between API requests (seconds) to be respectful
        """
        self.output_dir = output_dir
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Daf Yomi Downloader (respectful automated access)'
        })
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def get_tractate_info(self, tractate_name: str) -> Optional[dict]:
        """Get tractate information by English name."""
        for tractate in TRACTATES:
            if tractate["english"].lower() == tractate_name.lower():
                return tractate
        return None
    
    def fetch_text(self, tractate: str, daf: int, side: str, source: str = "main") -> Tuple[bool, str]:
        """
        Fetch text from Sefaria API.
        
        Args:
            tractate: English name of tractate
            daf: Daf number
            side: 'a' or 'b'
            source: "main" for base text or a commentary name (e.g., "Steinsaltz", "Rashi", "Tosafot")
            
        Returns:
            (success, text) tuple
        """
        if source == "main":
            url = f"https://www.sefaria.org/api/texts/{tractate}.{daf}{side}?lang=he&commentary=0&context=0"
        else:
            url = f"https://www.sefaria.org/api/texts/{source} on {tractate}.{daf}{side}?lang=he&context=0"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            hebrew_text = data.get('he', [])
            if isinstance(hebrew_text, list):
                text = '\n'.join(hebrew_text)
            else:
                text = str(hebrew_text) if hebrew_text else ""
            
            return True, text
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {tractate} {daf}{side}: {e}")
            return False, f"Error fetching: {e}"
        except Exception as e:
            print(f"Unexpected error for {tractate} {daf}{side}: {e}")
            return False, f"Unexpected error: {e}"
    
    def download_daf(
        self,
        tractate: str,
        daf: int,
        include_steinsaltz: bool = True,
        include_rashi: bool = True,
        include_tosafot: bool = True,
    ) -> bool:
        """
        Download a single daf (both sides) with optional commentary.
        
        Args:
            tractate: English name of tractate
            daf: Daf number
            include_steinsaltz: Whether to download Steinsaltz commentary
            include_rashi: Whether to download Rashi commentary
            include_tosafot: Whether to download Tosafot commentary
            
        Returns:
            True if successful, False otherwise
        """
        tractate_info = self.get_tractate_info(tractate)
        if not tractate_info:
            print(f"Tractate '{tractate}' not found")
            return False
        
        if daf < 2 or daf > tractate_info["daf_count"]:
            print(f"Daf {daf} is out of range for {tractate} (2-{tractate_info['daf_count']})")
            return False
        
        print(f"Downloading {tractate} {daf}...")
        
        # Fetch both sides
        combined_text = ""
        combined_steinsaltz = ""
        combined_rashi = ""
        combined_tosafot = ""
        sides = ['a', 'b']
        
        for side in sides:
            print(f"  Fetching {daf}{side}...")
            
            # Fetch main text
            success, text = self.fetch_text(tractate, daf, side, source="main")
            if success and text.strip():
                combined_text += f"--- {daf}{side} ---\n{text}\n\n"
            elif success:
                combined_text += f"--- {daf}{side} ---\n[No text available]\n\n"
            else:
                combined_text += f"--- {daf}{side} ---\n{text}\n\n"
            
            time.sleep(self.delay)
            
            # Fetch Steinsaltz
            if include_steinsaltz:
                print(f"  Fetching {daf}{side} Steinsaltz...")
                success, commentary_text = self.fetch_text(tractate, daf, side, source="Steinsaltz")
                if success and commentary_text.strip():
                    combined_steinsaltz += f"--- {daf}{side} ---\n{commentary_text}\n\n"
                elif success:
                    combined_steinsaltz += f"--- {daf}{side} ---\n[No commentary available]\n\n"
                else:
                    combined_steinsaltz += f"--- {daf}{side} ---\n{commentary_text}\n\n"
                time.sleep(self.delay)

            # Fetch Rashi
            if include_rashi:
                print(f"  Fetching {daf}{side} Rashi...")
                success, rashi_text = self.fetch_text(tractate, daf, side, source="Rashi")
                if success and rashi_text.strip():
                    combined_rashi += f"--- {daf}{side} ---\n{rashi_text}\n\n"
                elif success:
                    combined_rashi += f"--- {daf}{side} ---\n[No Rashi available]\n\n"
                else:
                    combined_rashi += f"--- {daf}{side} ---\n{rashi_text}\n\n"
                time.sleep(self.delay)

            # Fetch Tosafot
            if include_tosafot:
                print(f"  Fetching {daf}{side} Tosafot...")
                success, tosafot_text = self.fetch_text(tractate, daf, side, source="Tosafot")
                if success and tosafot_text.strip():
                    combined_tosafot += f"--- {daf}{side} ---\n{tosafot_text}\n\n"
                elif success:
                    combined_tosafot += f"--- {daf}{side} ---\n[No Tosafot available]\n\n"
                else:
                    combined_tosafot += f"--- {daf}{side} ---\n{tosafot_text}\n\n"
                time.sleep(self.delay)
        
        # Save main text
        main_filename = os.path.join(self.output_dir, f"{tractate}_{daf}.txt")
        try:
            with open(main_filename, 'w', encoding='utf-8') as f:
                f.write(combined_text)
            print(f"  Saved: {main_filename}")
        except Exception as e:
            print(f"  Error saving {main_filename}: {e}")
            return False
        
        # Save Steinsaltz if available
        if include_steinsaltz and combined_steinsaltz.strip():
            commentary_filename = os.path.join(self.output_dir, f"{tractate}_{daf}_steinsaltz.txt")
            try:
                with open(commentary_filename, 'w', encoding='utf-8') as f:
                    f.write(combined_steinsaltz)
                print(f"  Saved: {commentary_filename}")
            except Exception as e:
                print(f"  Error saving {commentary_filename}: {e}")

        # Save Rashi if available
        if include_rashi and combined_rashi.strip():
            rashi_filename = os.path.join(self.output_dir, f"{tractate}_{daf}_rashi.txt")
            try:
                with open(rashi_filename, 'w', encoding='utf-8') as f:
                    f.write(combined_rashi)
                print(f"  Saved: {rashi_filename}")
            except Exception as e:
                print(f"  Error saving {rashi_filename}: {e}")

        # Save Tosafot if available
        if include_tosafot and combined_tosafot.strip():
            tosafot_filename = os.path.join(self.output_dir, f"{tractate}_{daf}_tosafot.txt")
            try:
                with open(tosafot_filename, 'w', encoding='utf-8') as f:
                    f.write(combined_tosafot)
                print(f"  Saved: {tosafot_filename}")
            except Exception as e:
                print(f"  Error saving {tosafot_filename}: {e}")
        
        return True
    
    def download_tractate(self, tractate: str, start_daf: int = 2, end_daf: Optional[int] = None, 
                         include_steinsaltz: bool = True,
                         include_rashi: bool = True,
                         include_tosafot: bool = True) -> bool:
        """
        Download an entire tractate or a range of dafs.
        
        Args:
            tractate: English name of tractate
            start_daf: Starting daf number (default: 2)
            end_daf: Ending daf number (default: last daf of tractate)
            include_steinsaltz: Whether to download Steinsaltz commentary
            include_rashi: Whether to download Rashi commentary
            include_tosafot: Whether to download Tosafot commentary
            
        Returns:
            True if all downloads successful, False otherwise
        """
        tractate_info = self.get_tractate_info(tractate)
        if not tractate_info:
            print(f"Tractate '{tractate}' not found")
            return False
        
        if end_daf is None:
            end_daf = tractate_info["daf_count"]
        
        if start_daf < 2:
            start_daf = 2
        if end_daf > tractate_info["daf_count"]:
            end_daf = tractate_info["daf_count"]
        
        print(f"Downloading {tractate} ({tractate_info['hebrew']}) - Dafs {start_daf} to {end_daf}")
        print(f"Steinsaltz: {'Yes' if include_steinsaltz else 'No'} | Rashi: {'Yes' if include_rashi else 'No'} | Tosafot: {'Yes' if include_tosafot else 'No'}")
        print("-" * 50)
        
        success_count = 0
        total_dafs = end_daf - start_daf + 1
        
        for daf in range(start_daf, end_daf + 1):
            if self.download_daf(
                tractate,
                daf,
                include_steinsaltz=include_steinsaltz,
                include_rashi=include_rashi,
                include_tosafot=include_tosafot,
            ):
                success_count += 1
            print(f"Progress: {success_count}/{total_dafs} dafs completed")
            print()
        
        print(f"Completed: {success_count}/{total_dafs} dafs downloaded successfully")
        return success_count == total_dafs
    
    def list_tractates(self):
        """List all available tractates."""
        print("Available Tractates:")
        print("-" * 50)
        for i, tractate in enumerate(TRACTATES, 1):
            print(f"{i:2d}. {tractate['english']:15} ({tractate['hebrew']:12}) - {tractate['daf_count']} dafs")

def main():
    parser = argparse.ArgumentParser(description='Automated Daf Yomi Downloader')
    parser.add_argument('--tractate', '-t', help='Tractate name (English)')
    parser.add_argument('--daf', '-d', type=int, help='Specific daf number')
    parser.add_argument('--start', '-s', type=int, default=2, help='Start daf (default: 2)')
    parser.add_argument('--end', '-e', type=int, help='End daf (default: last daf)')
    parser.add_argument('--output', '-o', default='downloads', help='Output directory (default: downloads)')
    parser.add_argument('--no-commentary', action='store_true', help='Skip Steinsaltz commentary')  # legacy flag
    parser.add_argument('--no-steinsaltz', action='store_true', help='Skip Steinsaltz commentary')
    parser.add_argument('--no-rashi', action='store_true', help='Skip Rashi commentary')
    parser.add_argument('--no-tosafot', action='store_true', help='Skip Tosafot commentary')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--list', '-l', action='store_true', help='List all tractates')
    
    args = parser.parse_args()
    
    downloader = DafYomiDownloader(output_dir=args.output, delay=args.delay)
    
    if args.list:
        downloader.list_tractates()
        return
    
    if not args.tractate:
        print("Please specify a tractate with --tractate or use --list to see available tractates")
        downloader.list_tractates()
        return
    
    # Commentary toggles
    include_steinsaltz = not (args.no_commentary or args.no_steinsaltz)
    include_rashi = not args.no_rashi
    include_tosafot = not args.no_tosafot
    
    if args.daf:
        # Download single daf
        success = downloader.download_daf(
            args.tractate,
            args.daf,
            include_steinsaltz=include_steinsaltz,
            include_rashi=include_rashi,
            include_tosafot=include_tosafot,
        )
        if success:
            print(f"\n✓ Successfully downloaded {args.tractate} {args.daf}")
        else:
            print(f"\n✗ Failed to download {args.tractate} {args.daf}")
            sys.exit(1)
    else:
        # Download tractate or range
        success = downloader.download_tractate(
            args.tractate,
            args.start,
            args.end,
            include_steinsaltz=include_steinsaltz,
            include_rashi=include_rashi,
            include_tosafot=include_tosafot,
        )
        if success:
            print(f"\n✓ Successfully downloaded {args.tractate}")
        else:
            print(f"\n✗ Some downloads failed for {args.tractate}")
            sys.exit(1)

if __name__ == "__main__":
    main() 