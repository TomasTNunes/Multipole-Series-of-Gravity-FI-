@echo off
echo Activate .env
call .env\Scripts\activate > nul
echo Run app...
python -m main.py > nul
deactivate > nul