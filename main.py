from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import users
from app.routers import candidate_profiles
from app.routers import resumes
from app.routers import recruiter_profiles
from app.routers import job_postings
from app.routers import dashboard
from app.routers import admin
from app.routers import ai_recruiter
from app.routers import job_applications
from app.core.config import settings

print(f"Database URL from settings: {settings.DATABASE_URL}")
print(f"Secret Key loaded: {'Yes' if settings.SECRET_KEY else 'No'}")

app = FastAPI(
    title="AI Match Connect API",
    description="API for AI Match Connect platform, connecting candidates and recruiters.",
    version="0.1.0"
)


origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    # "https://www.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)

@app.get("/health", status_code=200)
def health_check():
    """
    Simple health check endpoint for the frontend to verify API connectivity.
    """
    return {"status": "ok"}

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(candidate_profiles.router, prefix=settings.API_V1_STR)
app.include_router(resumes.router, prefix=settings.API_V1_STR)
app.include_router(recruiter_profiles.router, prefix=settings.API_V1_STR)
app.include_router(job_postings.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(ai_recruiter.router, prefix=settings.API_V1_STR)
app.include_router(job_applications.router, prefix=settings.API_V1_STR)
@app.get("/")
async def root():
    return {"message": "Welcome to AI Match Connect API!"}



