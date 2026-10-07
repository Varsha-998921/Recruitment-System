import streamlit as st
import pandas as pd
from pathlib import Path
from utils import extract_pdf_text, extract_text_file, save_analysis, load_history, init_db
from matcher import calculate_match

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "data" / "sample_resumes"

st.set_page_config(
    page_title="AI Recruitment Recommendation System",
    page_icon="🤖",
    layout="wide"
)

init_db()

st.title("🤖 AI-Based Recruitment Recommendation System")
st.caption("AI-assisted candidate matching and ranking using NLP")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose", ["Candidate Ranking", "Analysis History", "About"])

if page == "Candidate Ranking":
    st.subheader("1. Enter Job Description")
    default_jd = (BASE_DIR / "sample_job_description.txt").read_text(encoding="utf-8")
    job_text = st.text_area(
        "Paste the job description here",
        value=default_jd,
        height=220
    )

    st.subheader("2. Upload Candidate Resumes")
    uploaded = st.file_uploader(
        "Upload PDF or TXT resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    st.info("For your first test, sample candidates are available below. You can also upload your own resumes.")

    if not uploaded:
        use_samples = st.checkbox("Use sample candidates", value=True)
    else:
        use_samples = False

    if st.button("🚀 Analyze Candidates", type="primary"):
        if not job_text.strip():
            st.error("Please enter a job description.")
            st.stop()

        candidates = []

        if uploaded:
            for file in uploaded:
                temp_path = BASE_DIR / "uploads" / file.name
                temp_path.write_bytes(file.getbuffer())
                try:
                    if file.name.lower().endswith(".pdf"):
                        resume_text = extract_pdf_text(temp_path)
                    else:
                        resume_text = extract_text_file(temp_path)
                except Exception as e:
                    st.warning(f"Could not read {file.name}: {e}")
                    continue
                candidates.append((Path(file.name).stem, file.name, resume_text))

        elif use_samples:
            for path in sorted(SAMPLE_DIR.glob("*.txt")):
                candidates.append((path.stem.replace("_", " ").title(), path.name, extract_text_file(path)))

        if not candidates:
            st.warning("Upload at least one resume or enable sample candidates.")
            st.stop()

        results = []
        for candidate_name, source_file, resume_text in candidates:
            result = calculate_match(job_text, resume_text)
            result.update({
                "candidate_name": candidate_name,
                "source_file": source_file
            })
            results.append(result)
            save_analysis(result)

        df = pd.DataFrame(results).sort_values("match_score", ascending=False).reset_index(drop=True)
        df.insert(0, "Rank", range(1, len(df) + 1))

        st.success(f"Analyzed {len(df)} candidate(s).")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Candidates", len(df))
        c2.metric("Top Score", f"{df.iloc[0]['match_score']:.1f}%")
        c3.metric("Strong Matches", int((df["recommendation"] == "Strong Match").sum()))
        c4.metric("Average Score", f"{df['match_score'].mean():.1f}%")

        st.subheader("🏆 Candidate Ranking")
        display = df[["Rank", "candidate_name", "match_score", "text_similarity", "skill_score", "recommendation"]].copy()
        display.columns = ["Rank", "Candidate", "Match Score %", "Text Similarity %", "Skill Score %", "Recommendation"]
        st.dataframe(display, use_container_width=True, hide_index=True)

        st.subheader("📊 Match Scores")
        chart_df = df.set_index("candidate_name")[["match_score"]]
        st.bar_chart(chart_df)

        st.subheader("🔎 Candidate Details")
        selected = st.selectbox("Select a candidate", df["candidate_name"].tolist())
        row = df[df["candidate_name"] == selected].iloc[0]

        left, right = st.columns(2)
        with left:
            st.write("**Matching Skills**")
            if row["matching_skills"]:
                for skill in row["matching_skills"]:
                    st.success(f"✓ {skill.title()}")
            else:
                st.write("No matching skills found.")

        with right:
            st.write("**Missing Skills**")
            if row["missing_skills"]:
                for skill in row["missing_skills"]:
                    st.warning(f"• {skill.title()}")
            else:
                st.success("No missing job skills detected.")

        st.write(f"**Recommendation:** {row['recommendation']}")
        st.write(f"**Final Match Score:** {row['match_score']}%")
        st.write(f"**Text Similarity:** {row['text_similarity']}%")
        st.write(f"**Skill Match:** {row['skill_score']}%")

elif page == "Analysis History":
    st.subheader("📚 Analysis History")
    history = load_history()
    if history.empty:
        st.info("No analyses have been stored yet.")
    else:
        st.dataframe(history, use_container_width=True, hide_index=True)
        csv = history.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download History CSV",
            csv,
            "recruitment_analysis_history.csv",
            "text/csv"
        )

else:
    st.subheader("About the Project")
    st.write("""
    This academic project uses Natural Language Processing (NLP) to compare
    job descriptions with candidate resumes. It combines TF-IDF text similarity
    and skill matching to produce a final candidate score and ranking.
    """)
    st.markdown("""
    **Architecture**

    Job Description → Text Processing → TF-IDF → Cosine Similarity  
    Resume → Text Extraction → Skill Extraction → Skill Matching  
    → Weighted Score → Candidate Ranking → Streamlit Dashboard → SQLite
    """)
    st.warning("The system is an AI-assisted screening tool for academic demonstration. Human review should always be used for real recruitment.")
