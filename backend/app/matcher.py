import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# BASE PATH (IMPORTANT FOR RENDER)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# LOAD MODEL ONCE
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# LOAD DATASET
# -----------------------------
jobs_path = os.path.join(BASE_DIR, "data", "jobs_final.csv")
emb_path = os.path.join(BASE_DIR, "data", "job_embeddings.npy")

jobs_df = pd.read_csv(jobs_path)

# Create combined text (used for UI display)
jobs_df["combined_text"] = (
    jobs_df["Job Title"].fillna("").astype(str)
    + " "
    + jobs_df["Description"].fillna("").astype(str)
)

# -----------------------------
# LOAD PRECOMPUTED EMBEDDINGS
# -----------------------------
job_embeddings = np.load(emb_path).astype(np.float32)

# Normalize job embeddings once (IMPORTANT for cosine similarity)
job_embeddings = job_embeddings / np.linalg.norm(
    job_embeddings,
    axis=1,
    keepdims=True
)

# -----------------------------
# MATCH FUNCTION
# -----------------------------
def match_jobs(resume_text, top_k=5):

    # Embed resume only (fast + lightweight)
    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    ).astype(np.float32)

    # Cosine similarity
    scores = cosine_similarity(resume_embedding, job_embeddings)[0]

    # Copy dataframe
    df = jobs_df.copy()
    df["score"] = scores

    # Sort results
    top_jobs = df.sort_values(
        by="score",
        ascending=False
    ).head(top_k)

    # Return frontend-friendly format
    return top_jobs[["combined_text", "score"]]