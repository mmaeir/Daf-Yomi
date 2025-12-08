# Automated Daf Yomi Downloader

This project automates downloading Hebrew Talmud texts and Steinsaltz commentary from Sefaria.org. It replicates the functionality of the web app but allows for bulk downloads and automation.

## Features

- Download individual dafs or entire tractates
- Includes main text plus Steinsaltz, Rashi, and Tosafot commentary (toggleable)
- Respectful API usage with configurable delays
- Progress tracking and error handling
- Supports all 40 tractates in the Babylonian Talmud
- Saves files in UTF-8 encoding for proper Hebrew display

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependency:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Examples

**List all available tractates:**
```bash
python daf_yomi_downloader.py --list
```

**Download a single daf:**
```bash
python daf_yomi_downloader.py --tractate Berakhot --daf 2
```

**Download an entire tractate:**
```bash
python daf_yomi_downloader.py --tractate Berakhot
```

**Download a range of dafs:**
```bash
python daf_yomi_downloader.py --tractate Berakhot --start 2 --end 10
```

**Download without commentary (Steinsaltz):**
```bash
python daf_yomi_downloader.py --tractate Berakhot --no-commentary
```

**Download only Rashi (skip Steinsaltz + Tosafot):**
```bash
python daf_yomi_downloader.py --tractate Berakhot --no-steinsaltz --no-tosafot
```

**Download without Rashi/Tosafot:**
```bash
python daf_yomi_downloader.py --tractate Berakhot --no-rashi --no-tosafot
```

### Command Line Options

- `--tractate, -t`: Tractate name (English) - required
- `--daf, -d`: Specific daf number (optional)
- `--start, -s`: Start daf (default: 2)
- `--end, -e`: End daf (default: last daf of tractate)
- `--output, -o`: Output directory (default: downloads)
- `--no-commentary` or `--no-steinsaltz`: Skip Steinsaltz commentary
- `--no-rashi`: Skip Rashi commentary
- `--no-tosafot`: Skip Tosafot commentary
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--list, -l`: List all tractates

### Advanced Examples

**Download to a specific directory:**
```bash
python daf_yomi_downloader.py --tractate Shabbat --output ./my_texts/
```

**Faster downloads (be respectful!):**
```bash
python daf_yomi_downloader.py --tractate Berakhot --delay 0.5
```

**Download multiple tractates (bash script):**
```bash
#!/bin/bash
tractates=("Berakhot" "Shabbat" "Eruvin")
for tractate in "${tractates[@]}"; do
    python daf_yomi_downloader.py --tractate "$tractate"
done
```

## File Output

Downloaded files are saved as:
- `{Tractate}_{Daf}.txt` - Main Hebrew text (both sides a and b)
- `{Tractate}_{Daf}_steinsaltz.txt` - Steinsaltz commentary (if available)
- `{Tractate}_{Daf}_rashi.txt` - Rashi commentary (if available)
- `{Tractate}_{Daf}_tosafot.txt` - Tosafot commentary (if available)

Example: `Berakhot_2.txt`, `Berakhot_2_steinsaltz.txt`, `Berakhot_2_rashi.txt`, `Berakhot_2_tosafot.txt`

## Available Tractates

The script supports all 40 tractates of the Babylonian Talmud:

### Seder Zeraim
- Berakhot (64 dafs)

### Seder Moed  
- Shabbat (157 dafs)
- Eruvin (105 dafs)
- Pesachim (121 dafs)
- Shekalim (22 dafs)
- Yoma (88 dafs)
- Sukkah (56 dafs)
- Beitzah (40 dafs)
- Rosh Hashanah (35 dafs)
- Taanit (31 dafs)
- Megillah (32 dafs)
- Moed Katan (29 dafs)
- Chagigah (27 dafs)

### Seder Nashim
- Yevamot (122 dafs)
- Ketubot (112 dafs)
- Nedarim (91 dafs)
- Nazir (66 dafs)
- Sotah (49 dafs)
- Gittin (90 dafs)
- Kiddushin (82 dafs)

### Seder Nezikin
- Bava Kamma (119 dafs)
- Bava Metzia (119 dafs)
- Bava Batra (175 dafs)
- Sanhedrin (113 dafs)
- Makkot (24 dafs)
- Shevuot (49 dafs)
- Avodah Zarah (76 dafs)
- Horayot (14 dafs)

### Seder Kodashim
- Zevachim (120 dafs)
- Menachot (110 dafs)
- Chullin (142 dafs)
- Bechorot (61 dafs)
- Arachin (34 dafs)
- Temurah (34 dafs)
- Keritot (28 dafs)
- Meilah (22 dafs)
- Kinnim (4 dafs)
- Tamid (10 dafs)
- Middot (4 dafs)

### Seder Taharot
- Niddah (73 dafs)

## Notes

- The script includes a 1-second delay between API requests by default to be respectful to Sefaria.org
- Files are saved in UTF-8 encoding to properly display Hebrew text
- Daf numbering starts from 2 (following traditional Talmud pagination)
- Not all dafs may have Steinsaltz commentary available
- The script handles errors gracefully and reports progress

## Data Source

All texts are downloaded from [Sefaria.org](https://www.sefaria.org), a free digital library of Jewish texts. Please respect their terms of service and API usage guidelines.

## Legal

This tool is for educational and personal study purposes. Please respect copyright and terms of service of the source material. 