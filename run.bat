@echo off
title AI Recruitment Recommendation System
echo ==============================================
echo AI Recruitment Recommendation System
echo ==============================================
if not exist .venv (
    echo Creating virtual environment...
    py -m venv .venv
)
call .venv\Scripts\activate
echo Installing/updating required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Starting Streamlit...
streamlit run app.py
pause
