from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from app.resume_parser import parse_resume
from app.matcher import match_jobs
from app.rag import ask_ai

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- UPLOAD FOLDER ----------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running"}

# ---------------- UPLOAD RESUME ----------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    text = parse_resume(file_path)

    return {
        "filename": file.filename,
        "text": text
    }

# ---------------- MATCH REQUEST MODEL ----------------
class MatchRequest(BaseModel):
    resume_text: str

# ---------------- JOB MATCHING API ----------------
@app.post("/match-jobs")
def match_jobs_api(request: MatchRequest):
    results = match_jobs(request.resume_text)

    return {
        "status": "success",
        "matches": results.to_dict(orient="records")
    }

# ---------------- AI CHAT REQUEST MODEL ----------------
class AskRequest(BaseModel):
    query: str

# ---------------- RAG CHATBOT API ----------------
@app.post("/ask-ai")
def ask_ai_endpoint(request: AskRequest):
    response = ask_ai(request.query)

    return {
        "status": "success",
        "answer": response
    }