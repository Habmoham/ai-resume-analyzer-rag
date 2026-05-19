from app.matcher import match_jobs

resume_text = """
I am a software engineer with experience in Python, FastAPI, and React.
I have built ML models and worked with NLP projects.
"""

results = match_jobs(resume_text)

print(results)