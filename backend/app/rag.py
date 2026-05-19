import requests
from app.vector_store import create_index, search_index


# -----------------------------
# STEP 1 — Build knowledge base ONCE
# -----------------------------
texts = [
    "A good resume should highlight skills clearly",
    "Tailor your resume to job description",
    "Use action verbs like built, created, developed",
    "Keep resume concise and under 1-2 pages",
    "Practice LeetCode for technical interviews",
    "Machine learning engineers should know Python, NLP, embeddings"
]

index, _ = create_index(texts)


# -----------------------------
# STEP 2 — Retrieve context
# -----------------------------
def retrieve_context(query):
    results = search_index(index, query, texts, top_k=3)
    return "\n".join(results)


# -----------------------------
# STEP 3 — Call Ollama
# -----------------------------
def generate_response(query, context):
    url = "http://localhost:11434/api/generate"

    prompt = f"""
You are an AI career assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{query}

Answer in simple professional language:
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()["response"]


# -----------------------------
# STEP 4 — MAIN FUNCTION
# -----------------------------
def ask_ai(query):
    context = retrieve_context(query)
    return generate_response(query, context)