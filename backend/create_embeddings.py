import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading dataset...")

jobs_df = pd.read_csv("../data/jobs_final.csv")

jobs_df["combined_text"] = (
    jobs_df["Job Title"].fillna("").astype(str)
    + " "
    + jobs_df["Description"].fillna("").astype(str)
)

job_texts = jobs_df["combined_text"].tolist()

print("Creating embeddings...")

job_embeddings = model.encode(
    job_texts,
    normalize_embeddings=True,
    show_progress_bar=True
)

np.save(
    "../data/job_embeddings.npy",
    job_embeddings
)

print("Embeddings saved successfully!")