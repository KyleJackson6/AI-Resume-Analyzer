import streamlit as st
from analyzer import match_skills
from file_reader import read_file, extract_relevant_sections
import os
import nltk
from io import StringIO
import base64

nltk.download("punkt")
nltk.download("punkt_tab")

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer")
st.markdown("""
Upload your **resume** and either upload a **job description file** or paste the job description text manually.
This tool compares your skills and experience against job requirements and provides clear, structured feedback.
""")

with st.expander("ℹ️ How it works"):
    st.markdown("""
    1. Upload your resume (PDF, DOCX, or TXT)
    2. Upload a job description file **or** paste it directly
    3. The app uses AI to find and compare key skills
    4. You’ll get a score, matched and missing skills, and feedback
    """)

ALLOWED_TYPES = [".txt", ".pdf", ".docx"]

resume_file = st.file_uploader("Upload Resume", type=ALLOWED_TYPES)
job_file = st.file_uploader("Upload Job Description", type=ALLOWED_TYPES)
job_text_input = st.text_area("Or paste the job description text directly:")

def generate_explanation(score, matched, missing, job_skills):
    explanation = f"### Match Analysis\n"
    explanation += f"This resume received a match score of **{score:.2f}%** based on a comparison of extracted skills and experience sections.\n\n"

    if matched:
        explanation += "**Matched Skills:**\n"
        for skill in sorted(matched):
            explanation += f"- {skill}\n"
    else:
        explanation += "No relevant skills were matched between the resume and the job description.\n"

    explanation += "\n"

    if missing:
        explanation += "**Missing Skills from Job Description:**\n"
        for skill in sorted(missing):
            explanation += f"- {skill}\n"
        explanation += "\n"
    else:
        explanation += "All major job description skills were found in the resume.\n"

    if score >= 75:
        explanation += "This resume aligns very well with the job requirements."
    elif score >= 40:
        explanation += "This resume shows some relevant skills, but also reveals key areas that could be strengthened."
    else:
        explanation += "This resume currently lacks several of the job's required skills and may benefit from further development."

    return explanation

def score_feedback(score):
    if score >= 75:
        return "🟢 Strong Match"
    elif score >= 40:
        return "🟡 Moderate Match"
    else:
        return "🔴 Weak Match"

def download_button(text, filename="analysis.txt"):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="color:white;background:#4CAF50;padding:0.5em 1em;text-decoration:none;border-radius:5px;">Download Analysis Report</a>'
    st.markdown(href, unsafe_allow_html=True)

if resume_file and (job_file or job_text_input.strip()):
    resume_ext = os.path.splitext(resume_file.name)[-1].lower()
    job_ext = os.path.splitext(job_file.name)[-1].lower() if job_file else None

    if resume_ext in ALLOWED_TYPES and (not job_file or job_ext in ALLOWED_TYPES):
        raw_resume_text = read_file(resume_file, resume_ext)

        if job_file:
            raw_job_text = read_file(job_file, job_ext)
        elif job_text_input.strip():
            raw_job_text = job_text_input.strip()
        else:
            raw_job_text = ""

        if raw_job_text.strip() == "":
            st.warning("We couldn't extract a usable job description. Please paste it manually or upload a file.")
        else:
            resume_text = extract_relevant_sections(raw_resume_text)
            job_text = extract_relevant_sections(raw_job_text)

            with st.spinner("Analyzing resume and job description..."):
                score, matched, resume_skills, job_skills = match_skills(resume_text, job_text)
                missing = job_skills - matched
                explanation = generate_explanation(score, matched, missing, job_skills)

            st.metric(label="Match Score", value=f"{score:.2f}%")
            st.markdown(f"**Assessment:** {score_feedback(score)}")
            st.progress(int(score))

            tab1, tab2, tab3 = st.tabs(["Summary", "Skill Breakdown", "Raw Data"])

            with tab1:
                st.markdown(explanation)
                download_button(explanation)
                st.info("💡 Tip: If you're missing key skills, consider adding relevant projects, certifications, or rephrasing existing experience in your resume.")

            with tab2:
                st.markdown("**Matched Skills:**")
                st.write(sorted(matched) if matched else "None")
                st.markdown("**Missing Skills from Job Description:**")
                st.write(sorted(missing) if missing else "None")

            with tab3:
                with st.expander("Resume Skills Extracted"):
                    st.write(sorted(resume_skills))
                with st.expander("Job Description Skills Extracted"):
                    st.write(sorted(job_skills))
                with st.expander("Preview Uploaded Resume"):
                    st.text(raw_resume_text[:1000])
                with st.expander("Preview Job Description"):
                    st.text(raw_job_text[:1000])

            if st.button("Clear Inputs"):
                st.experimental_rerun()

    else:
        st.error("Only .txt, .pdf, and .docx files are supported.")