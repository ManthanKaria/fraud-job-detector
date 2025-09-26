from fastapi import APIRouter
import datetime

router=APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow()
    }