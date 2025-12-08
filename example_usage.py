#!/usr/bin/env python3
"""
Example usage of the DafYomiDownloader class
This shows how to use the downloader programmatically in your own scripts
"""

from daf_yomi_downloader import DafYomiDownloader

def main():
    # Create a downloader instance
    # Output will go to 'example_downloads' folder with 0.5 second delays
    downloader = DafYomiDownloader(output_dir="example_downloads", delay=0.5)
    
    print("=== Daf Yomi Downloader Example ===\n")
    
    # Example 1: List all tractates
    print("1. Available tractates:")
    downloader.list_tractates()
    print("\n" + "="*50 + "\n")
    
    # Example 2: Download a single daf
    print("2. Downloading Berakhot 2...")
    success = downloader.download_daf("Berakhot", 2, include_commentary=True)
    if success:
        print("✓ Successfully downloaded Berakhot 2")
    else:
        print("✗ Failed to download Berakhot 2")
    print("\n" + "="*50 + "\n")
    
    # Example 3: Download a small range (first 3 dafs of Berakhot)
    print("3. Downloading Berakhot dafs 3-5...")
    success = downloader.download_tractate("Berakhot", start_daf=3, end_daf=5, include_commentary=True)
    if success:
        print("✓ Successfully downloaded Berakhot 3-5")
    else:
        print("✗ Some downloads failed for Berakhot 3-5")
    print("\n" + "="*50 + "\n")
    
    # Example 4: Download without commentary
    print("4. Downloading Berakhot 6 (no commentary)...")
    success = downloader.download_daf("Berakhot", 6, include_commentary=False)
    if success:
        print("✓ Successfully downloaded Berakhot 6 (no commentary)")
    else:
        print("✗ Failed to download Berakhot 6")
    print("\n" + "="*50 + "\n")
    
    print("Example completed! Check the 'example_downloads' folder for the downloaded files.")

if __name__ == "__main__":
    main() 