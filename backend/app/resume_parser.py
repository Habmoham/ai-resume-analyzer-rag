import fitz  # PyMuPDF
import pdfplumber

def extract_text_pymupdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_pdfplumber(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def clean_text(text):
    # simple cleaning
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def parse_resume(file_path):
    # try PyMuPDF first
    text = extract_text_pymupdf(file_path)

    # fallback if empty
    if not text.strip():
        text = extract_text_pdfplumber(file_path)

    return clean_text(text)