@echo off
title R10 Web X-RAY
color 0C
cls

echo ===================================================
echo   R10 WEB X-RAY - STARTING
echo ===================================================
echo.

pip install -r requirements.txt >nul 2>&1
python main.py
pause