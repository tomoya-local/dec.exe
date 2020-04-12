@echo off
pyinstaller dec2.py -F -i lockfile.ico --exclude tkinter --exclude xml
pause