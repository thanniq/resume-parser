from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pdfminer.high_level import extract_text
import requests
import tempfile

app = FastAPI()

class ResumeRequest(BaseModel):
    resumeUrl: str

@app.post("/parse-resume")
def parse_resume(req: ResumeRequest):
    try:
        response = requests.get(req.resumeUrl)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid PDF URL")

        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp.flush()
            text = extract_text(tmp.name)

        return {"success": True, "resumeText": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))