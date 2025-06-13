import streamlit as st
from tools.document_reader import load_deviation_text
from tools.rag_index import *
from capa_agent import summarize_deviation, classify_root_cause, suggest_capa, rag_summarize

st.title("CAPA Reasoning Agent")

uploaded_file = st.file_uploader("Upload deviation report", type=["txt"])

if uploaded_file:
    
    text = load_deviation_text(uploaded_file)

    st.subheader("Deviation Text")
    st.text(text)

    # Use RAG to summarize by retrieving top docs + summarizing
    summary = rag_summarize(text)

    st.subheader("Summarized Deviation")
    st.info(summary)

    # Classify based on the summary, not raw text
    root_cause = classify_root_cause(summary)
    capa_plan = suggest_capa(root_cause)

    st.subheader("Inferred Root Cause")
    st.success(root_cause)

    st.subheader("Suggested Corrective Action")
    st.write(capa_plan["corrective"])

    st.subheader("Suggested Preventive Action")
    st.write(capa_plan["preventive"])
