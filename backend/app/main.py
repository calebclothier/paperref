""" Entry point for running the FastAPI backend app.
"""
from fastapi import FastAPI
from app.routers import auth, graph, papers, recommended


# Create the FastAPI app instance
app = FastAPI(
    title="PaperRef API",
    description="Backend API for PaperRef web app",
    version="0.1.0",
)


# Add all routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(papers.router, prefix="/library", tags=["library"])
app.include_router(graph.router, prefix="/graph", tags=["graph"])
app.include_router(recommended.router, prefix="/recommended", tags=["recommended"])


# Root endpoint for testing
@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"message": "API is up and running!"}
=======
    """
    Dummy route for testing purposes

    Returns:
        dict: "API is up and running!"
    """
    return {"message": "API is up and running!"}
>>>>>>> 9487df3 (add: added docstrings and static typying)
