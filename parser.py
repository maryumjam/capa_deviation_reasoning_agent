import os
import re
import json


def extract_section(text, keyword):
    """Find section content by keyword"""
    pattern = rf"{keyword}[:\n](.*?)(?=\n[A-Z][a-zA-Z ]+:|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None

def parse_txt_document(file_path, doc_type):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if doc_type.lower() == "sop":
        return {
            "type": "SOP",
            "title": extract_section(text, "Title"),
            "author": extract_section(text, "Author"),
            "date": extract_section(text, "Date"),
            "purpose": extract_section(text, "Purpose"),
            "scope": extract_section(text, "Scope"),
            "procedure_steps": extract_section(text, "Procedure"),
            "responsibilities": extract_section(text, "Responsibilities"),
        }
    elif doc_type.lower() == "capa":
        return {
            "type": "CAPA",
            "title": extract_section(text, "Title"),
            "author": extract_section(text, "Author"),
            "date": extract_section(text, "Date"),
            "root_cause": extract_section(text, "Root Cause"),
            "corrective_action": extract_section(text, "Corrective Action"),
            "preventive_action": extract_section(text, "Preventive Action"),
            "effectiveness_check": extract_section(text, "Effectiveness Check"),
        }

def parse_all_documents(base_path):
    parsed_docs = []

    for doc_type in ['SOP', 'CAPA']:
        folder_path = os.path.join(base_path, doc_type)
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                parsed = parse_txt_document(file_path, doc_type)
                parsed['filename'] = filename
                parsed_docs.append(parsed)

    return parsed_docs

if __name__ == "__main__":
    base_path = "data"
    results = parse_all_documents(base_path)
    with open("parsed_documents.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Parsed documents saved to parsed_documents.json")
