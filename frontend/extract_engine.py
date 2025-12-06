import os
from pathlib import Path
import pdfplumber
from docx import Document

# --- Ustawienia ---
UPLOAD_FOLDER = "uploads"
TEXT_OUTPUT_FOLDER = "uploads_text"
CHUNK_SIZE_WORDS = 1000  # liczba słów w jednym pliku

os.makedirs(TEXT_OUTPUT_FOLDER, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return text


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text


def save_full_text(text, file_base_name):
    # folder: uploads_text/[nazwa_pliku].txt
    output_file = os.path.join(TEXT_OUTPUT_FOLDER, f"{file_base_name}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)


def process_file(file_path):
    file_name = os.path.basename(file_path)
    file_base_name = os.path.splitext(file_name)[0]

    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        print(f"Nieobsługiwany format: {file_path}")
        return

    save_full_text(text, file_base_name)
    print(f"Przetworzono {file_name}, zapisano cały tekst w {TEXT_OUTPUT_FOLDER}/{file_base_name}.txt")
