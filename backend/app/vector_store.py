import faiss
import numpy as np

def create_index(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    if len(embeddings.shape) != 2:
        raise ValueError("Embeddings must be 2D")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings


def search_index(index, query_vec, texts, top_k=5):

    query_vec = np.array(query_vec).astype("float32")

    if len(query_vec.shape) == 1:
        query_vec = query_vec.reshape(1, -1)

    distances, indices = index.search(query_vec, top_k)

    results = []
    for i in indices[0]:
        if i < len(texts):
            results.append(texts[i])

    return results