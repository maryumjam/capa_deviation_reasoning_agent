import os
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

INDEX_PATH = "data/vector_store/faiss_index.bin"
DOCS_PATH = "data/vector_store/docs.npy"
META_PATH = "data/vector_store/meta.npy"
MODEL_NAME = "all-MiniLM-L6-v2"

def build_vector_store(doc_folder="data/docs/"):
    os.makedirs("data/vector_store", exist_ok=True)
    model = SentenceTransformer(MODEL_NAME)

    texts, metadata = [], []
    for fname in os.listdir(doc_folder):
        with open(os.path.join(doc_folder, fname), "r") as f:
            text = f.read()
            texts.append(text)
            metadata.append(fname)

    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and associated data
    faiss.write_index(index, INDEX_PATH)
    np.save(DOCS_PATH, np.array(texts, dtype=object))
    np.save(META_PATH, np.array(metadata, dtype=object))

    print(f"🔍 Vector store built with {len(texts)} documents.")

    return model, index, texts, metadata


def load_vector_store():
    model = SentenceTransformer(MODEL_NAME)
    index = faiss.read_index(INDEX_PATH)
    texts = np.load(DOCS_PATH, allow_pickle=True)
    metadata = np.load(META_PATH, allow_pickle=True)
    return model, index, texts.tolist(), metadata.tolist()


def retrieve_similar(text, model, index, texts, metadata, k=3):
    query_embedding = model.encode([text])
    D, I = index.search(query_embedding, k)
    return [(texts[i], metadata[i]) for i in I[0]]
