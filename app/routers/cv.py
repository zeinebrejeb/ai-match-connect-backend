from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.models.user import User 
from app.dependencies import deps 
from app.schemas.cv import CVAnalysisResponse 
from app.services import cv_analyser 


router = APIRouter(
    prefix="/cv",
    tags=["cv"], # Tag for API documentation
    responses={404: {"description": "Not found"}},
)

@router.post("/upload-analyze", response_model=CVAnalysisResponse)
async def upload_and_analyze_cv(
    file: UploadFile = File(...), 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_active_user) 
) -> Any:
    """
    Uploads a CV (PDF), analyzes it using AI (simulated), and returns extracted data.
    """
    # --- File Validation ---
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are allowed."
        )


    try:
        extracted_data = await cv_analyser.simulate_cv_analysis(file)
        # In a real app, you might save the extracted_data to the user's profile here
        # For example:
        # crud.candidate_profile.update_from_cv_data(db, profile=current_user.candidate_profile, data=extracted_data)

    except Exception as e:
        # Catch potential errors during file processing or analysis
        print(f"Error during CV analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze CV. Please try again or enter information manually."
        )


    return CVAnalysisResponse(extractedData=extracted_data)

# Note: You might add other CV-related endpoints here later,
# e.g., GET /cv/me to see the last analyzed data (if saved)
# or endpoints to manage the raw uploaded CV files.

