# AI-Based Recruitment Recommendation and Candidate Ranking System

A free, local B.Tech CSE project that analyzes job descriptions and candidate resumes, calculates AI-based matching scores, identifies matching/missing skills, and ranks candidates.

## Technology
- Python
- Streamlit
- NLP
- TF-IDF
- Cosine Similarity
- SQLite
- Pandas
- PyPDF2
- Scikit-learn

## Run on Windows

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The browser will open the Streamlit dashboard.

## Project flow

Job Description + Resumes
-> PDF/Text Extraction
-> NLP preprocessing
-> TF-IDF
-> Cosine Similarity
-> Skill Matching
-> Weighted Match Score
-> Candidate Ranking
-> SQLite Database
-> Streamlit Dashboard

## Important
This project is an academic decision-support system. It should not be used as the sole basis for real hiring decisions. Human review is required.
"# Recruitment-System" 
"# Recruitment-System" 
