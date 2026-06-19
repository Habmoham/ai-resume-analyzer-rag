import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Config
MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = Path("data/jobs_final.csv")
OUTPUT_PATH = Path("data/job_embeddings.npy")

# Load model
print(f"Loading model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)

# Load data
print("Loading dataset...")
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

jobs_df = pd.read_csv(DATA_PATH)

# Build input text
jobs_df["combined_text"] = (
    jobs_df["Job Title"].fillna("").astype(str)
    + " "
    + jobs_df["Description"].fillna("").astype(str)
)

job_texts = jobs_df["combined_text"].tolist()

# Generate embeddings
print("Creating embeddings...")
job_embeddings = model.encode(
    job_texts,
    normalize_embeddings=True,
    show_progress_bar=True
)

# Save embeddings
print("Saving embeddings...")
np.save(OUTPUT_PATH, job_embeddings)

# Save metadata
metadata = {
    "model_name": MODEL_NAME,
    "embedding_dim": job_embeddings.shape[1],
    "num_jobs": len(job_texts)
}

np.save("data/embedding_metadata.npy", metadata, allow_pickle=True)

print("Done: embeddings + metadata saved")