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

# -----------------------------
# CREATE combined_text
# -----------------------------
jobs_df["combined_text"] = (
    jobs_df["Job Title"].fillna("").astype(str)
    + " "
    + jobs_df["Description"].fillna("").astype(str)
)

# -----------------------------
# LOAD PRECOMPUTED EMBEDDINGS
# -----------------------------
job_embeddings = np.load(
    "../data/job_embeddings.npy"
)

# -----------------------------
# MATCH FUNCTION
# -----------------------------
def match_jobs(resume_text, top_k=5):

    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
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

    # keep frontend compatibility
    top_jobs["combined_text"] = (
        top_jobs["Job Title"].astype(str)
        + " "
        + top_jobs["Description"].astype(str)
    )

    return top_jobs[
        ["combined_text", "score"]
    ]