import faiss
import numpy as np

# -----------------------------
# CREATE VECTOR INDEX
# -----------------------------
def create_index(embeddings):
    """
    embeddings: List or np.array of shape (num_items, embedding_dim)
    """

    embeddings = np.array(embeddings).astype("float32")

    # Safety check (VERY IMPORTANT)
    if len(embeddings.shape) != 2:
        raise ValueError("Embeddings must be a 2D array (num_items, embedding_dim)")

    dim = embeddings.shape[1]

    # FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    return index, embeddings


# -----------------------------
# SEARCH INDEX
# -----------------------------
def search_index(index, query_vec, texts, top_k=5):
    """
    query_vec: embedding vector from Hugging Face API
    texts: original text list (job descriptions etc.)
    """

    query_vec = np.array(query_vec).astype("float32")

    # Ensure correct shape for FAISS (1, dim)
    if len(query_vec.shape) == 1:
        query_vec = query_vec.reshape(1, -1)

    distances, indices = index.search(query_vec, top_k)

    results = []

    for i in indices[0]:
        if i < len(texts):
            results.append(texts[i])

    return results