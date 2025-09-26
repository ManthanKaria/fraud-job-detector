from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np


from app.utils.preprocess import clean_text

router = APIRouter(prefix="/predict", tags=["predictions"])

# Load the trained model at startup
MODEL_PATH = os.path.join("app", "models", "fake_job_model.pkl")
model = joblib.load(MODEL_PATH)


class JobDescription(BaseModel):
    description: str | None = None
    text: str | None = None


@router.post("/")
def predict_fraud(data: JobDescription):
    # accept description OR text
    raw_text = (data.description or data.text or "").strip()
    cleaned = clean_text(raw_text)

    if not cleaned or len(cleaned) < 10:
        raise HTTPException(
            status_code=400, detail="Description too short after cleaning"
        )

    try:
        # model expects preprocessed text (TF-IDF inside pipeline)
        prediction = model.predict([cleaned])[0]
        # predict_proba may return two probabilities; take max
        if hasattr(model, "predict_proba"):
            probability = float(np.max(model.predict_proba([cleaned])[0]))
        else:
            # fallback if model doesn't support predict_proba
            probability = 1.0

        return {
            "fraudulent": bool(prediction),
            "confidence": round(probability, 3) if probability is not None else None,
            "cleaned_text": cleaned,  # useful for debugging & frontend display
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
