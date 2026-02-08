from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- INSTALL THIS: pip install flask-cors
from services.ai_service import analyze_with_gemini
from services.github_service import fetch_github_data
from services.pdf_service import extract_text_from_pdf
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # <--- This allows your HTML to talk to Python

@app.route('/analyze', methods=['POST'])
def analyze():
    # 1. Check for data (Supports both 'github_user' and 'username')
    user = request.form.get('github_user') or request.form.get('username')
    resume = request.files.get('resume')

    if not user or not resume:
        return jsonify({"error": "Missing data"}), 400

    try:
        # 2. Extract Data
        print(f"[*] Processing user: {user}")
        resume_text = extract_text_from_pdf(resume)
        github_stats = fetch_github_data(user)

        # 3. AI Analysis
        # We wrap the result in a JSON object with the key 'analysis'
        # so your HTML (data.analysis) can read it.
        report = analyze_with_gemini(resume_text, github_stats)
        
        return jsonify({"analysis": report})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"analysis": f"<div class='alert alert-danger'>Server Error: {str(e)}</div>"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)