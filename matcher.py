from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import clean_text, extract_skills

def calculate_match(job_text, resume_text):
    job_clean = clean_text(job_text)
    resume_clean = clean_text(resume_text)

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([job_clean, resume_clean])
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    text_score = similarity * 100

    job_skills = set(extract_skills(job_text))
    resume_skills = set(extract_skills(resume_text))

    matching = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)

    skill_score = (len(matching) / len(job_skills) * 100) if job_skills else 0
    final_score = (0.60 * text_score) + (0.40 * skill_score)

    if final_score >= 80:
        recommendation = "Strong Match"
    elif final_score >= 60:
        recommendation = "Good Match"
    elif final_score >= 40:
        recommendation = "Moderate Match"
    else:
        recommendation = "Low Match"

    return {
        "match_score": round(final_score, 2),
        "text_similarity": round(text_score, 2),
        "skill_score": round(skill_score, 2),
        "matching_skills": matching,
        "missing_skills": missing,
        "recommendation": recommendation
    }
