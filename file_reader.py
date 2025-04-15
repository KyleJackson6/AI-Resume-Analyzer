import pdfplumber
from docx import Document

def read_file(file, file_type: str) -> str:
    if file_type == ".txt":
        return file.read().decode("utf-8")

    elif file_type == ".pdf":
        with open("temp.pdf", "wb") as temp_file:
            temp_file.write(file.read())
        with pdfplumber.open("temp.pdf") as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif file_type == ".docx":
        with open("temp.docx", "wb") as temp_file:
            temp_file.write(file.read())
        doc = Document("temp.docx")
        return "\n".join([para.text for para in doc.paragraphs])

    return ""

def extract_relevant_sections(text: str) -> str:
    lines = text.lower().splitlines()
    relevant = []
    capture = False
    keywords = ["responsibilities", "qualifications", "requirements", "skills", "experience", "about you"]

    for line in lines:
        if any(k in line for k in keywords):
            capture = True
        if capture and line.strip():
            relevant.append(line.strip())

    # Fallback: return whole text if no keyword section found
    return "\n".join(relevant) if relevant else text
