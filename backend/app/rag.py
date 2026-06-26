import requests
import os
from app.vector_store import create_index, search_index
from app.config import GROQ_API_KEY


if not GROQ_API_KEY:
     print("WARNING: GROQ_API_KEY not set")

# -----------------------------
# STEP 1 — Build knowledge base
# -----------------------------
texts = [
    "A good resume should highlight skills clearly",
    "Tailor your resume to job description",
    "Use action verbs like built, created, developed",
    "Keep resume concise and under 1-2 pages",
    "Practice LeetCode for technical interviews",
    "Machine learning engineers should know Python, NLP, embeddings"
]

# -----------------------------
# GLOBAL INDEX (lazy loaded)
# -----------------------------
index = None

# -----------------------------
# STEP 2 — Lazy load FAISS index
# -----------------------------
def get_index():
    global index

    if index is None:
        index, _ = create_index(texts)

    return index


# -----------------------------
# STEP 3 — Retrieve context
# -----------------------------
def retrieve_context(query):
    idx = get_index()

    results = search_index(
        idx,
        query,
        texts,
        top_k=3
    )

    return "\n".join(results)


# -----------------------------
# STEP 4 — Generate AI response
# -----------------------------
def generate_response(query, context):

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        prompt = f"""
You are an AI career assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{query}

Answer in a professional and helpful way.
"""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI career assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        if response.status_code != 200:
            return response.text

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", str(e))
        return str(e)


# -----------------------------
# STEP 5 — MAIN FUNCTION
# -----------------------------
def ask_ai(query):
    context = retrieve_context(query)
    return generate_response(query, context)