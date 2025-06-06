# backend/text_preprocessor.py
import re
import string
import joblib
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

class TextPreprocessor:
    def __init__(self, text_attribute="text"):
        self.text_attribute = text_attribute

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"\d+", "", text)  # Remove numbers
        text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
        text = " ".join(word for word in text.split() if word not in STOPWORDS)  # Remove stopwords
        return text

    def transform(self, texts):
        return [self.clean_text(text) for text in texts]
