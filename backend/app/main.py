from fastapi import FastAPI

from app.routers import auth


# Create the FastAPI app instance
app = FastAPI(
    title="PaperRef API",
    description="Backend API for PaperRef web app",
    version="0.1.0"
)

# Include the authentication router
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Optional: root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "API is up and running!"}