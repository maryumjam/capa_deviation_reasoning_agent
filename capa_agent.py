from transformers import pipeline
import streamlit as st
def classify_root_cause(text):
    text_lower = text.lower()
    if "calibration" in text_lower or "misaligned" in text_lower:
        return "Mechanical Failure"
    elif "operator" in text_lower or "training" in text_lower:
        return "Human Error"
    elif "contamination" in text_lower or "cleaning" in text_lower:
        return "Process Hygiene"
    elif "label" in text_lower:
        return "Documentation/Labeling Error"
    return "Uncategorized"

def suggest_capa(root_cause):
    capa_suggestions = {
        "Mechanical Failure": {
            "corrective": "Repair or replace faulty equipment.",
            "preventive": "Implement routine maintenance schedule."
        },
        "Human Error": {
            "corrective": "Retrain involved personnel.",
            "preventive": "Enhance SOP clarity; schedule regular training."
        },
        "Process Hygiene": {
            "corrective": "Re-clean affected areas; discard affected batches.",
            "preventive": "Revise cleaning protocols and verification checks."
        },
        "Documentation/Labeling Error": {
            "corrective": "Recall affected labels/products.",
            "preventive": "Introduce version control and cross-check protocols."
        },
        "Uncategorized": {
            "corrective": "Escalate to QA team for manual review.",
            "preventive": "Collect more data for trend analysis."
        }
    }
    return capa_suggestions.get(root_cause, capa_suggestions["Uncategorized"])

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_deviation(text):
    summarizer = get_summarizer()
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']


from tools.rag_index import load_vector_store, retrieve_similar
from transformers import pipeline

model, index, texts, metadata = load_vector_store()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def rag_summarize(query_text, top_k=3):
    docs = retrieve_similar(query_text, model, index, texts, metadata, k=top_k)
    combined_text = "\n\n".join([doc for doc, _ in docs])
    summary = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']
