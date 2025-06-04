from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# Configure Gemini (use environment variable)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("message", "")
    try:
        response = model.generate_content(prompt)
        plain_text = re.sub(r'<.*?>|\*{1,2}([^*]+)\*{1,2}', r'\1', response.text)
        return jsonify({"response": plain_text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) 
