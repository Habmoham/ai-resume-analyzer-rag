import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# BASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# -----------------------------
# GLOBALS (LAZY LOADING)
# -----------------------------
model = None
jobs_df = None
job_embeddings = None


# -----------------------------
# LOAD RESOURCES ONLY WHEN NEEDED
# -----------------------------
def load_resources():

    global model
    global jobs_df
    global job_embeddings

    # -----------------------------
    # LOAD MODEL ONLY ONCE
    # -----------------------------
    if model is None:

        print("Loading SentenceTransformer model...")

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # -----------------------------
    # LOAD DATASET ONLY ONCE
    # -----------------------------
    if jobs_df is None:

        print("Loading jobs dataset...")

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
    # LOAD EMBEDDINGS ONLY ONCE
    # -----------------------------
    if job_embeddings is None:

        print("Loading embeddings...")

        emb_path = os.path.join(
            BASE_DIR,
            "data",
            "job_embeddings.npy"
        )

        job_embeddings = np.load(
            emb_path
        ).astype(np.float32)

        # -----------------------------
        # NORMALIZE EMBEDDINGS ONCE
        # -----------------------------
        norms = np.linalg.norm(
            job_embeddings,
            axis=1,
            keepdims=True
        )

        # Prevent division by zero
        norms[norms == 0] = 1

        job_embeddings = (
            job_embeddings / norms
        )

    return model, jobs_df, job_embeddings


# -----------------------------
# MATCH FUNCTION
# -----------------------------
def match_jobs(
    resume_text,
    top_k=5
):

    # Load resources lazily
    model, jobs_df, job_embeddings = load_resources()

    # -----------------------------
    # ENCODE RESUME
    # -----------------------------
    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    ).astype(np.float32)

    # -----------------------------
    # COSINE SIMILARITY
    # -----------------------------
    scores = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    # -----------------------------
    # ADD SCORES
    # -----------------------------
    df = jobs_df.copy()

    df["score"] = scores

    # -----------------------------
    # TOP MATCHES
    # -----------------------------
    top_jobs = df.sort_values(
        by="score",
        ascending=False
    ).head(top_k)

    return top_jobs[
        ["combined_text", "score"]
    ]