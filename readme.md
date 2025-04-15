# AI Resume Analyzer

This is a web-based application that compares a resume to a job description and provides a match score along with insights into matched and missing skills. It uses natural language processing (NLP) and BERT-based semantic similarity to evaluate alignment between job requirements and candidate qualifications.

## Features

- Upload resume (PDF, DOCX, or TXT)
- Upload or paste job description text
- Receive a match score and skill comparison
- Highlights matched and missing keywords
- Professional feedback and downloadable analysis report
- Built with Streamlit for quick web-based deployment

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv resume_env
# Activate the environment:
# On macOS/Linux:
source resume_env/bin/activate
# On Windows:
resume_env\\Scripts\\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## File Structure

- `app.py` – Main Streamlit application
- `analyzer.py` – Handles skill extraction and BERT-based semantic comparison
- `file_reader.py` – Manages file reading and relevant section extraction
- `requirements.txt` – Python dependencies
- `.gitignore` – Files and folders excluded from version control

## License

This project is licensed under the MIT License.
