from fastapi import APIRouter
from pydantic import BaseModel
import joblib ,os
import numpy as np

router=APIRouter(
    prefix="/explain",
    tags=["explanations"]
)

# Load the trained model at startup
MODEL_PATH = os.path.join("app","models","fake_job_model.pkl")
model = joblib.load(MODEL_PATH)

class JobDescription(BaseModel):
    description: str            

@router.post("/")
def explain_prediction(data: JobDescription):
    # Extracting tfidf and clf from the pipeline
    vectorizer = model.named_steps['tfidf']
    clf = model.named_steps['clf']
    
    X=vectorizer.transform([data.description])
    features = vectorizer.get_feature_names_out()
    coefs = clf.coef_[0]
    
    # Top positive and negative features
    scores = X.toarray()[0] * coefs
    top_idx=np.argsort(scores)[-5:][::-1]
    top_features = {features[i]: round(scores[i], 3) for i in top_idx}
    
    return {
        "top_features": top_features,
        "note": "Positive scores indicate features contributing to a fraudulent prediction, while negative scores indicate features contributing to a non-fraudulent prediction."
    }