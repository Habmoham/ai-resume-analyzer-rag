from fastapi import APIRouter, UploadFile, File
import os
from resume_parser import parse_resume

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 🔥 USE YOUR FULL PARSER (PyMuPDF + fallback + cleaning)
    extracted_text = parse_resume(file_path)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "path": file_path,
        "text": extracted_text
    }