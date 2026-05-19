import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')


# -----------------------------
# Load cleaned job dataset
# -----------------------------
def load_jobs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "..", "data", "cleaned_jobs.csv")

    df = pd.read_csv(file_path)
    return df


# -----------------------------
# Match resume with jobs
# -----------------------------
def match_jobs(resume_text, top_k=5):
    jobs = load_jobs()

    # IMPORTANT: use combined_text
    job_texts = jobs["combined_text"].fillna("").tolist()

    # Embed
    resume_embedding = model.encode([resume_text])
    job_embeddings = model.encode(job_texts)

    # Similarity
    scores = cosine_similarity(resume_embedding, job_embeddings)[0]

    jobs["score"] = scores

    # Sort results
    top_jobs = jobs.sort_values(by="score", ascending=False).head(top_k)

    return top_jobs[["combined_text", "score"]]