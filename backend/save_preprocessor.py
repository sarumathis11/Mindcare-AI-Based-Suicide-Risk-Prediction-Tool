from text_preprocessor import TextPreprocessor
import joblib

# Create an instance of TextPreprocessor
text_preprocessor = TextPreprocessor()

# Save the instance to a joblib file
joblib.dump(text_preprocessor, "text_preprocessor.joblib")

print("TextPreprocessor object has been saved successfully!")
