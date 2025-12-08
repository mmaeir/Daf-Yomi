@echo off
REM Daf Yomi Downloader - Windows Batch Examples
REM Make sure Python and requirements are installed first

echo ========================================
echo Daf Yomi Downloader - Example Commands
echo ========================================
echo.

echo 1. Installing requirements...
pip install -r requirements.txt
echo.

echo 2. Listing all available tractates...
python daf_yomi_downloader.py --list
echo.
pause

echo 3. Downloading a single daf (Berakhot 2)...
python daf_yomi_downloader.py --tractate Berakhot --daf 2
echo.
pause

echo 4. Downloading a range of dafs (Berakhot 2-5)...
python daf_yomi_downloader.py --tractate Berakhot --start 2 --end 5
echo.
pause

echo 5. Downloading without commentary (Berakhot 6)...
python daf_yomi_downloader.py --tractate Berakhot --daf 6 --no-commentary
echo.
pause

echo 6. Running programmatic example...
python example_usage.py
echo.
pause

echo.
echo ========================================
echo All examples completed!
echo Check the 'downloads' and 'example_downloads' folders
echo ========================================
pause 