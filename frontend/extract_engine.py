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


def chunk_text(text, chunk_size=CHUNK_SIZE_WORDS):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks


def save_chunks(chunks, file_base_name):
    # folder: uploads_text/[nazwa_pliku]/
    output_dir = os.path.join(TEXT_OUTPUT_FOLDER, file_base_name)
    os.makedirs(output_dir, exist_ok=True)

    for idx, chunk in enumerate(chunks, start=1):
        chunk_file = os.path.join(output_dir, f"{idx}.txt")
        with open(chunk_file, "w", encoding="utf-8") as f:
            f.write(chunk)


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

    chunks = chunk_text(text)
    save_chunks(chunks, file_base_name)
    print(
        f"Przetworzono {file_name} -> {len(chunks)} chunków w {TEXT_OUTPUT_FOLDER}/{file_base_name}/"
    )
