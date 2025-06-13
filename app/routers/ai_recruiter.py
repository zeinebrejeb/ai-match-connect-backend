import httpx
import os
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Dict
from app import crud
from app.database.database import get_db 
from pydantic import BaseModel

class AISearchRequest(BaseModel):
    job_id: int 
    candidate_ids: List[int]

router = APIRouter(
    prefix="/ai-recruiter",
    tags=["AI Recruiter"],
    responses={404: {"description": "Not found"}},
)

AGENTIC_RAG_API_URL = os.getenv("AGENTIC_RAG_API_URL", "http://127.0.0.1:8001/agentic-screen")

@router.post("/search", response_model=Dict[str, Any])
async def search_with_ai(
    request_body: AISearchRequest = Body(...),

    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint for the Recruiter AI Search functionality.
    """
    print(f"--- AI Search Endpoint: Received request for Job ID: {request_body.job_id} ---")

    print("Retrieving job and candidate data from the database...")
    
    db_job = await crud.job.get(db, id=request_body.job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail=f"Job with ID {request_body.job_id} not found.")
    
    db_resumes = [
        {"id": cid, "resume_text": f"This is the resume text for candidate {cid}."} for cid in request_body.candidate_ids
    ]
    if not db_resumes:
        raise HTTPException(status_code=404, detail="No matching candidates found for the provided IDs.")

    resumes_for_agent = []
    for resume in db_resumes:
        resume_id = resume.get("id")
        resume_text = resume.get("resume_text")
        if resume_text:
             resumes_for_agent.append({"id": str(resume_id), "text": resume_text})
        else:
            print(f"Warning: Resume ID {resume_id} is missing text content and will be skipped.")

    if not resumes_for_agent:
        raise HTTPException(status_code=400, detail="None of the selected candidates have resume text to analyze.")

    agentic_rag_payload = {
        "job_id": str(request_body.job_id),
        "job_description_text": db_job.description, 
        "resumes": resumes_for_agent
    }
    
    print(f"Data prepared. Calling AgenticRAG service at: {AGENTIC_RAG_API_URL}")

    async with httpx.AsyncClient(timeout=300.0) as client: 
        try:
            response = await client.post(AGENTIC_RAG_API_URL, json=agentic_rag_payload)
            response.raise_for_status()
        except httpx.ConnectError as e:
            raise HTTPException(status_code=503, detail=f"AI service unavailable: {e}")
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json().get("detail", e.response.text)
            raise HTTPException(status_code=502, detail=f"AI service failed: {error_detail}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    print("Successfully received response from AgenticRAG service.")
    return response.json()
