import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import auth_bp, init_bcrypt

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = '2755c0df13cf42ab17ee9cfa6679b892495addf7ee74d7134c3d8c02300a7b5e'

# Initialize Bcrypt
init_bcrypt(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

# Gemini API Key Configuration
GEMINI_API_KEY = "AIzaSyB_e78uenctaAkC1G0JvjIwKBElZIhqkt4"
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
