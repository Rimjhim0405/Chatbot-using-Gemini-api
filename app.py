from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os


app = Flask(__name__)


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
        return jsonify({"response": response.text}) # Send the raw Markdown
    except Exception as e:
        # It's good practice to log the full error for debugging
        print(f"Error calling Gemini API: {e}") 
        # For frontend, return a user-friendly message
        return jsonify({"response": "An error occurred while getting a response. Please try again."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
