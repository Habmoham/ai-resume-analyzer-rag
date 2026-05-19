import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')


# -----------------------------
# CREATE VECTOR INDEX
# -----------------------------
def create_index(texts):
    embeddings = model.encode(texts)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(np.array(embeddings).astype('float32'))

    return index, embeddings


# -----------------------------
# SEARCH INDEX
# -----------------------------
def search_index(index, query, texts, top_k=5):
    query_vec = model.encode([query]).astype('float32')

    distances, indices = index.search(query_vec, top_k)

    results = []
    for i in indices[0]:
        results.append(texts[i])

    return results