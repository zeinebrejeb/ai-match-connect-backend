from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
import pypdf # pip install pypdf
import io

from app.database.database import get_db
from app.models.candidate_profile import CandidateProfile 
# Assuming you have a CRUD function to update a candidate
from app.crud.crud_candidate_profile import candidate_profile as crud_candidate
from app.dependencies.deps import get_current_active_candidate

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post(
    "/upload",
    # Define a response model if you want, e.g., a simple status message
    status_code=status.HTTP_200_OK, 
    summary="Upload and Extract Text from a Resume",
    description="Uploads a candidate's resume (PDF), extracts the text, and saves it to their profile.",
)
async def upload_resume(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    current_candidate: CandidateProfile = Depends(get_current_active_candidate),
) -> dict:
    """
    This endpoint handles the one-time action of a candidate uploading their resume.
    1. Validates the file is a PDF.
    2. Extracts the raw text from the PDF.
    3. Saves the extracted text to the candidate's profile in the database.
    4. Optionally, you could save the original PDF to a file storage (e.g., S3) here.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are allowed."
        )

    try:
        pdf_content = await file.read()
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_content))
        
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or "" # Add a fallback for empty pages

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract any text from the PDF. The file might be an image-based PDF or corrupted."
            )
            
        # Update the candidate's profile with the extracted text
        # You need a CRUD function like this. The `resume_text` field must be added to your CandidateProfile model.
        update_data = {"resume_text": extracted_text}
        await crud_candidate.update(db=db, db_obj=current_candidate, obj_in=update_data)

        # You can also save the original file here if needed
        # For example: save_to_s3(pdf_content, f"resumes/{current_candidate.id}.pdf")
        
        return {
            "detail": "Resume uploaded and processed successfully.",
            "fileName": file.filename,
            "text_length": len(extracted_text)
        }

    except Exception as e:
        print(f"Error during resume processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume. Error: {str(e)}"
        )