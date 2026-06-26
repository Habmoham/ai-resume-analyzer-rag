import os

# Only load dotenv locally (Render ignores .env automatically)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not set")

if not HF_API_KEY:
    print("WARNING: HF_API_KEY not set")