@echo off
cd /d "%~dp0"
if "%~1"=="" (
  py -3 render.py
) else (
  py -3 render.py "%~1"
)
pause
