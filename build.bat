@echo off
pyinstaller --noconfirm --onefile --windowed --icon=SlicerDHub.ico --hidden-import=win32gui --hidden-import=win32api --hidden-import=win32con --hidden-import=win32ui SlicerDHub.py
pause
