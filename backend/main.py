from fastapi import FastAPI, UploadFile, File
from resume_parser import extract_resume_text
from ai_analyzer import analyze_resume
from matcher import match_resume_to_jobs
from ai_matcher import ai_match_resume
from database import SessionLocal
from models import Resume 
from internship_service import get_all_internships  
import json
from fastapi.middleware.cors import CORSMiddleware
from models import Application
from database import SessionLocal

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
    allow_origins=[
        "https://internship-copilot-test1.vercel.app",
        "http://localhost:5173"
    ],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Internship Copilot API"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    contents = await file.read()

    with open("resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_resume_text("resume.pdf")

    db = SessionLocal()

    resume = Resume(
        filename=file.filename,
        resume_text=resume_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    db.close()

    return {
        "resume_id": resume.id,
        "filename": resume.filename
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/internships")
def get_internships():
    return get_all_internships()

@app.post("/match-resume")
async def match_resume(file: UploadFile = File(...)):

    contents = await file.read()

    with open("resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_resume_text("resume.pdf")

    matches = match_resume_to_jobs(
        resume_text,
        sample_jobs
    )

    return matches

@app.post("/ai-match")
async def ai_match(file: UploadFile = File(...)):

    contents = await file.read()

    with open("resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_resume_text("resume.pdf")

    db = SessionLocal()

    applied = db.query(Application).all()

    applied_urls = [
        app.url
        for app in applied
        
    ]

    db.close()


    jobs = get_all_internships()


    # Remove already applied internships
    jobs = [
        job for job in jobs
        if job["url"] not in applied_urls
    ]


    results = ai_match_resume(
        resume_text,
        jobs
    )

    return results

@app.get("/test-internships")
def test_internships():

    jobs = get_all_internships()

    return jobs

@app.post("/apply")
def apply(job: dict):

    db = SessionLocal()

    application = Application(
        company=job["company"],
        title=job["title"],
        url=job["url"],
        status="applied"
    )

    db.add(application)
    db.commit()

    db.close()

    return {
        "message": "Application saved"
    }