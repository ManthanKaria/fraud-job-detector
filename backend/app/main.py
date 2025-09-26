from fastapi import FastAPI
from app.routers import prediction
from app.routers import explain
from app.routers import health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fraud Job Detection API",
    description="API for detecting fraudulent job postings using a trained ML model.",
    version="1.0.0",
)

origins = ["http://localhost:3000", "http://your-frontend-vercel-domain.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # local Next.js dev
        "http://127.0.0.1:3000",  # alternate local
        "https://your-frontend-vercel-domain.vercel.app",  # deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(prediction.router)
app.include_router(explain.router)
app.include_router(health.router)


@app.get("/")
def read_root():
    return {"message": "Fraud Job Detection API is running."}
