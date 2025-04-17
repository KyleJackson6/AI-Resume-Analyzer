from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import subprocess
import sys

# Load or download the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer("all-mpnet-base-v2")

def extract_phrases(text: str):
    doc = nlp(text.lower())
    return list({chunk.text.strip() for chunk in doc.noun_chunks if 2 <= len(chunk.text.split()) <= 6})

def filter_skills(phrases):
    keywords = [
        "python", "sql", "tensorflow", "docker", "ai", "machine learning", "cloud", "pandas",
        "keras", "emr", "fhir", "data", "git", "nlp", "analytics", "platform", "tool"
    ]
    return [p for p in phrases if any(k in p.lower() for k in keywords)]

def match_skills(resume_text: str, job_text: str):
    resume_phrases = extract_phrases(resume_text)
    job_phrases = extract_phrases(job_text)

    resume_phrases = filter_skills(resume_phrases)
    job_phrases = filter_skills(job_phrases)

    if not resume_phrases or not job_phrases:
        return 0.0, set(), set(), set()

    resume_embeddings = model.encode(resume_phrases, convert_to_tensor=True)
    job_embeddings = model.encode(job_phrases, convert_to_tensor=True)

    matched = set()
    for i, job_phrase in enumerate(job_phrases):
        job_vec = job_embeddings[i].unsqueeze(0)
        sims = cosine_similarity(job_vec, resume_embeddings)[0]
        if max(sims) > 0.4:
            matched.add(job_phrase)

    job_set = set(job_phrases)
    score = (len(matched) / len(job_set)) * 100 if job_set else 0
    return score, matched, set(resume_phrases), job_set
