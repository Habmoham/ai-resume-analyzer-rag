import os
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from huggingface_hub import InferenceClient

from app.config import HF_API_KEY


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


jobs_df = None
job_embeddings = None


# -----------------------------
# HUGGING FACE CLIENT
# -----------------------------
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_KEY
)


# -----------------------------
# LOAD RESOURCES LAZY
# -----------------------------
def load_resources():

    global jobs_df
    global job_embeddings


    # -----------------------------
    # LOAD JOB DATA
    # -----------------------------
    if jobs_df is None:

        jobs_path = os.path.join(
            BASE_DIR,
            "data",
            "jobs_final.csv"
        )

        jobs_df = pd.read_csv(
            jobs_path
        )


        jobs_df["combined_text"] = (
            jobs_df["Job Title"]
            .fillna("")
            .astype(str)
            +
            " "
            +
            jobs_df["Description"]
            .fillna("")
            .astype(str)
        )


    # -----------------------------
    # LOAD JOB EMBEDDINGS
    # -----------------------------
    if job_embeddings is None:

        emb_path = os.path.join(
            BASE_DIR,
            "data",
            "job_embeddings.npy"
        )


        job_embeddings = np.load(
            emb_path
        ).astype(np.float32)


        # Normalize embeddings
        norms = np.linalg.norm(
            job_embeddings,
            axis=1,
            keepdims=True
        )


        norms[norms == 0] = 1


        job_embeddings = (
            job_embeddings / norms
        )


    return jobs_df, job_embeddings



# -----------------------------
# GET RESUME EMBEDDING
# -----------------------------
def get_embedding(text):


    try:

        output = client.feature_extraction(
            text,
            model="sentence-transformers/all-MiniLM-L6-v2"
        )


        embedding = np.array(
            output,
            dtype=np.float32
        )


        # If model returns token embeddings
        if len(embedding.shape) == 2:
            embedding = embedding.mean(axis=0)


        # Normalize
        norm = np.linalg.norm(
            embedding
        )


        if norm != 0:
            embedding = embedding / norm


        return embedding.reshape(
            1,
            -1
        )


    except Exception as e:

        print(
            "HuggingFace ERROR:",
            str(e)
        )

        raise e



# -----------------------------
# MATCH JOBS
# -----------------------------
def match_jobs(
    resume_text,
    top_k=5
):


    jobs_df, job_embeddings = load_resources()


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
        [
            "combined_text",
            "score"
        ]
    ]