from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from backend.resume_parser import extract_text_from_pdf
from ai_service import analyze_resume
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Resume Analyzer")

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:

        # Process in memory so uploaded resumes are not retained on disk.
        resume_text = extract_text_from_pdf(await file.read())

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        analysis = analyze_resume(resume_text)

        return {
            "filename": file.filename,
            "message": "Resume analyzed successfully",
            "analysis": analysis
        }

    except HTTPException:
        raise

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
