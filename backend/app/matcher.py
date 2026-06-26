import os
import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.config import HF_API_KEY


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# -----------------------------
# LOAD DATASET
# -----------------------------
jobs_path = os.path.join(
    BASE_DIR,
    "data",
    "jobs_final.csv"
)

jobs_df = pd.read_csv(jobs_path)

jobs_df["combined_text"] = (
    jobs_df["Job Title"]
    .fillna("")
    .astype(str)
    + " "
    +
    jobs_df["Description"]
    .fillna("")
    .astype(str)
)

# -----------------------------
# LOAD EMBEDDINGS
# -----------------------------
emb_path = os.path.join(
    BASE_DIR,
    "data",
    "job_embeddings.npy"
)

job_embeddings = np.load(
    emb_path
).astype(np.float32)

# normalize once
norms = np.linalg.norm(
    job_embeddings,
    axis=1,
    keepdims=True
)

norms[norms == 0] = 1

job_embeddings = job_embeddings / norms


# -----------------------------
# HUGGING FACE EMBEDDING API
# -----------------------------
API_URL = (
    "https://api-inference.huggingface.co/"
    "pipeline/feature-extraction/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def get_embedding(text):

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": text
        }
    )

    output = response.json()

    embedding = np.array(
        output
    ).mean(axis=0)

    embedding = embedding.astype(
        np.float32
    )

    # normalize
    norm = np.linalg.norm(embedding)

    if norm != 0:
        embedding = embedding / norm

    return embedding.reshape(1, -1)


# -----------------------------
# MATCH FUNCTION
# -----------------------------
def match_jobs(
    resume_text,
    top_k=5
):

    resume_embedding = get_embedding(
        resume_text
    )

    scores = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    df = jobs_df.copy()

    df["score"] = scores

    top_jobs = df.sort_values(
        by="score",
        ascending=False
    ).head(top_k)

    return top_jobs[
        ["combined_text", "score"]
    ]