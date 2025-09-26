import joblib
import pandas as pd
from sklearn.metrics import classification_report

# Load trained model
model = joblib.load("../outputs/fake_job_model.pkl")

# Load test data
df = pd.read_csv("../data/fake_job_postings.csv")
df = df[['description', 'fraudulent']].dropna()
X_test = df['description']
y_test = df['fraudulent']

# Predict & Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
