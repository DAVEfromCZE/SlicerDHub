@echo off
set "VERSION=0.32"
set "NAME=SlicerDHub_v%VERSION%.exe"

pyinstaller --noconfirm --onefile --windowed --icon=SlicerDHub.ico --hidden-import=win32gui --hidden-import=win32api --hidden-import=win32con --hidden-import=win32ui slicerdhub.py

rename dist\slicerdhub.exe %NAME%
echo Build complete: dist\%NAME%
pause