import requests
import numpy as np
from app.vector_store import create_index, search_index
from app.config import GROQ_API_KEY

# ---------------- SAFETY CHECK ----------------
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in environment variables")

texts = [
    "A good resume should highlight skills clearly",
    "Tailor your resume to job description",
    "Use action verbs like built, created, developed",
    "Keep resume concise and under 1-2 pages",
    "Practice LeetCode for technical interviews",
    "Machine learning engineers should know Python, NLP, embeddings"
]

index = None

def get_index():
    global index
    if index is None:
        index, _ = create_index(texts)
    return index

def retrieve_context(query):
    idx = get_index()

    results = search_index(
        idx,
        query,
        texts,
        top_k=3
    )

    return "\n".join(results)

# ---------------- GROQ CALL (HARDENED) ----------------
def generate_response(query, context):

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        prompt = f"""
You are an AI career assistant.

Context:
{context}

Question:
{query}

Answer clearly and professionally.
"""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful AI career assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()

        # ✅ HARD CHECK
        if "choices" not in data:
            raise ValueError(f"Groq API error: {data}")

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("GROQ ERROR:", str(e))
        return f"Error: {str(e)}"


def ask_ai(query):
    context = retrieve_context(query)
    return generate_response(query, context)