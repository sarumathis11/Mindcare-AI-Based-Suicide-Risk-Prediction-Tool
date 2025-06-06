from flask import Blueprint, request, jsonify
import pickle
import joblib
import numpy as np
from text_preprocessor import TextPreprocessor
import joblib

# Load the saved model and vectorizer
model = joblib.load("suicide_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")
suicide_bp = Blueprint("suicide", __name__)

# Load trained models
models = [
    pickle.load(open("models/VotingClassifier_Text_classification.pkl", "rb")),
    pickle.load(open("models/SGDClassifier_Text_classification.pkl", "rb")),
    pickle.load(open("models/LinearSVC_Text_classification.pkl", "rb")),
    pickle.load(open("models/LogisticRegression_Text_classification.pkl", "rb")),
    pickle.load(open("models/ComplementNB_Text_classification.pkl", "rb"))
]

# Load text preprocessor and vectorizer
text_preprocessor = joblib.load("text_preprocessor.joblib")  # Now it will work!
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Function to predict suicide intent
def predict_suicide(text):
    processed_text = text_preprocessor.transform([text])  # Apply preprocessing
    text_vectorized = vectorizer.transform(processed_text)  # Convert to numerical vector
    text_array = text_vectorized.toarray()

    predictions = [model.predict(text_array)[0] for model in models]
    result = np.bincount(predictions).argmax()  # Majority voting

    return "Suicide Alert!" if result == 1 else "Sample AI Response"

# API Route for Classification
@suicide_bp.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    user_text = data.get("text")

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    response = predict_suicide(user_text)
    return jsonify({"response": response})
