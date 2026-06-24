import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# LOAD MODEL ONCE
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# LOAD DATASET
# -----------------------------
jobs_df = pd.read_csv("../data/jobs_final.csv")

jobs_df["combined_text"] = (
    jobs_df["Job Title"].fillna("").astype(str)
    + " "
    + jobs_df["Description"].fillna("").astype(str)
)

# -----------------------------
# LOAD PRECOMPUTED EMBEDDINGS
# -----------------------------
job_embeddings = np.load("../data/job_embeddings.npy")

# IMPORTANT: ensure float32 (faster + safer)
job_embeddings = job_embeddings.astype(np.float32)

# -----------------------------
# MATCH FUNCTION
# -----------------------------
def match_jobs(resume_text, top_k=5):

    # embed resume (normalize BOTH sides for correctness)
    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    ).astype(np.float32)

    # also normalize job embeddings (VERY IMPORTANT)
    job_emb_norm = job_embeddings / np.linalg.norm(
        job_embeddings,
        axis=1,
        keepdims=True
    )

    scores = cosine_similarity(
        resume_embedding,
        job_emb_norm
    )[0]

    df = jobs_df.copy()
    df["score"] = scores

    top_jobs = df.sort_values(
        by="score",
        ascending=False
    ).head(top_k)

    return top_jobs[["combined_text", "score"]]