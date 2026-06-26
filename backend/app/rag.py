import requests

from app.vector_store import (
    create_index,
    search_index
)

from app.config import GROQ_API_KEY


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

        embeddings = [
            [0.1]*384,
            [0.2]*384,
            [0.3]*384,
            [0.4]*384,
            [0.5]*384,
            [0.6]*384
        ]

        index, _ = create_index(
            embeddings
        )

    return index


def retrieve_context(query):

    idx = get_index()

    query_vector = [[0.5]*384]

    results = search_index(
        idx,
        query_vector,
        texts,
        top_k=3
    )

    return "\n".join(results)


def generate_response(
    query,
    context
):

    if not GROQ_API_KEY:

        return "Missing GROQ API key"

    try:

        url = (
            "https://api.groq.com/"
            "openai/v1/chat/completions"
        )

        prompt = f"""
Context:
{context}

Question:
{query}
"""

        payload = {

            "model":
            "llama-3.3-70b-versatile",

            "messages":[
                {
                    "role":"system",
                    "content":"You are an AI career assistant."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        }

        headers = {
            "Authorization":
            f"Bearer {GROQ_API_KEY}",
            "Content-Type":
            "application/json"
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        data = response.json()

        if "choices" not in data:

            return f"API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        return str(e)


def ask_ai(query):

    context = retrieve_context(query)

    return generate_response(
        query,
        context
    )