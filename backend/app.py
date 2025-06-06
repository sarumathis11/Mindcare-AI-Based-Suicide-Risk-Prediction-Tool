import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import auth_bp, init_bcrypt

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'API_KEY'

# Initialize Bcrypt
init_bcrypt(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

# Gemini API Key Configuration
GEMINI_API_KEY = "API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/gemini/chat", methods=["POST"])
def gemini_chat():
    try:
        data = request.get_json()
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"response": "Please provide a valid input."})

        model = genai.GenerativeModel("gemini-1.5-pro")  # Use the correct model name

        response = model.generate_content(user_input)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
