# tools/document_reader.py

import os
import fitz  # PyMuPDF


def load_deviation_text(file):
    return file.read().decode("utf-8")


def read_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def read_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_deviation_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return read_text_from_pdf(filepath)
    elif ext == ".txt":
        return read_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
