import re
import sqlite3
from pathlib import Path
from datetime import datetime
from PyPDF2 import PdfReader

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "recruitment.db"

SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript",
    "html", "css", "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "git", "github",
    "flask", "django", "streamlit", "power bi", "excel",
    "data analysis", "data visualization", "statistics",
    "aws", "azure", "docker", "linux", "react"
]

def extract_pdf_text(path):
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def extract_text_file(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text):
    cleaned = clean_text(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, cleaned):
            found.append(skill)
    return sorted(set(found))

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analyzed_at TEXT NOT NULL,
                candidate_name TEXT NOT NULL,
                source_file TEXT NOT NULL,
                match_score REAL NOT NULL,
                text_similarity REAL NOT NULL,
                skill_score REAL NOT NULL,
                matching_skills TEXT,
                missing_skills TEXT,
                recommendation TEXT
            )
        """)
        con.commit()

def save_analysis(row):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            INSERT INTO analyses
            (analyzed_at, candidate_name, source_file, match_score,
             text_similarity, skill_score, matching_skills,
             missing_skills, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row["candidate_name"],
            row["source_file"],
            row["match_score"],
            row["text_similarity"],
            row["skill_score"],
            ", ".join(row["matching_skills"]),
            ", ".join(row["missing_skills"]),
            row["recommendation"]
        ))
        con.commit()

def load_history():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        return __import__("pandas").read_sql_query(
            "SELECT * FROM analyses ORDER BY id DESC", con
        )
