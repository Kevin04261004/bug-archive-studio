@echo off
cd /d "%~dp0"
py -3 render.py --batch episodes
pause
