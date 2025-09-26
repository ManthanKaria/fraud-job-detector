import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import os


from utils.preprocess import clean_text

# Step 1: Load Dataset
DATA_PATH = "./data/fake_job_postings.csv"
df = pd.read_csv("./data/fake_job_postings.csv")

# Keep only necessary columns
df = df[['description', 'fraudulent']].dropna()

# Apply cleaning to the descriptions
df['description'] = df['description'].astype(str).apply(clean_text)

X = df['description']
y = df['fraudulent']

# Step 2: Split Dataset in terms of train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,stratify=y
)

# Step 3: Create a Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english',max_features=5000)),
    ('clf', LogisticRegression(solver='liblinear',class_weight='balanced'))
])

# Step 4: Hyperparameter Tuning
param_grid = {
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'clf__C': [0.1, 1, 10],
    'clf__penalty': ['l1', 'l2']
}

grid = GridSearchCV(pipeline, param_grid, cv=3,scoring='f1', n_jobs=-1, verbose=2)
grid.fit(X_train, y_train)

# Step 5: Evaluate the Model
y_pred = grid.predict(X_test)
print("Best Parameters:", grid.best_params_)
print(classification_report(y_test, y_pred))

# Step 6: Save the Model and Vectorizer
os.makedirs('../outputs', exist_ok=True)
joblib.dump(grid.best_estimator_, '../outputs/fake_job_model.pkl')
print("Model saved to ../outputs/fake_job_model.pkl")


## Run Trainning from ML Directory then only it will run