from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

print("Backend starting...")

app = Flask(__name__)
import logging

# Basic logging setup
logging.basicConfig(level=logging.INFO)

def handle_error(e, user_msg="Something went wrong"):
    logging.error(str(e))
    return jsonify({"error": user_msg, "details": str(e)})
CORS(app)

try:
    from ai_helper import call_ai
    AI_AVAILABLE = True
    print("AI helper loaded successfully")
except Exception as e:
    print("AI helper failed to load:", e)
    AI_AVAILABLE = False
    
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text


@app.route("/")
def home():
    return "Study Genie Backend is running!"


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        text = request.json.get("text", "").strip()
        difficulty = request.json.get("difficulty", "Medium")
        if not text:
            return jsonify({"summary": "Please provide some notes to summarize."})
        if not AI_AVAILABLE:
            return jsonify({"summary": "AI is not available. Check your API key."})

        prompt = f"""Summarize the following study notes in a clear and concise way.
Use bullet points. Keep it under 150 words.

Notes:
{text[:3000]}
"""
        result = call_ai(prompt)
        return jsonify({"summary": result})
    except Exception as e:
        return handle_error(e, "Error generating summary")


@app.route("/questions", methods=["POST"])
def questions():
    try:
        text = request.json.get("text", "").strip()
        difficulty = request.json.get("difficulty", "Medium")

        if not text:
            return jsonify({"questions": "Please provide notes."})

        if not AI_AVAILABLE:
            return jsonify({"questions": "AI not available."})

        prompt = f"""
Generate EXACTLY 7 questions of ONLY {difficulty.upper()} difficulty.

STRICT RULES:
- Do NOT include EASY/MEDIUM/HARD labels
- Do NOT mix difficulty levels
- All 7 questions must match {difficulty.upper()} level ONLY
- No repetition
- Each question must be from a different concept

Difficulty definition:
- EASY → basic definitions, direct facts
- MEDIUM → conceptual understanding, application
- HARD → analytical, reasoning, scenario-based

OUTPUT FORMAT:
1. Question
2. Question
3. Question
...

Notes:
{text[:4000]}
"""

        result = call_ai(prompt)
        return jsonify({"questions": result})

    except Exception as e:
        return handle_error(e, "Error generating questions")


@app.route("/mcq", methods=["POST"])
def mcq():
    try:
        text = request.json.get("text", "").strip()
        difficulty = request.json.get("difficulty", "Medium")
        if not text:
            return jsonify({"mcq": "Please provide some notes to generate MCQs from."})
        if not AI_AVAILABLE:
            return jsonify({"mcq": "AI is not available. Check your API key."})

        prompt = f"""Generate 5 {difficulty.upper()} level MCQs.

Format each MCQ exactly like this:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [Correct letter]

Notes:
{text[:3000]}
"""
        result = call_ai(prompt)
        return jsonify({"mcq": result})
    except Exception as e:
        return handle_error(e, "Error generating MCQs")
    
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"text": "No file uploaded"})

        extracted_text = extract_text_from_pdf(file)

        if not extracted_text.strip():
            return jsonify({"text": "Could not extract text from PDF"})

        return jsonify({"text": extracted_text})

    except Exception as e:
        return handle_error(e, "Error processing PDF")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        question = request.json.get("question", "").strip()
        context = request.json.get("context", "").strip()
        if not question:
            return jsonify({"answer": "Please type a question."})
        if not AI_AVAILABLE:
            return jsonify({"answer": "AI is not available. Check your API key."})

        prompt = f"""You are a helpful study assistant. Answer the student's question based only on the notes provided.
If the answer is not in the notes, say "I could not find that in your notes."

Study Notes:
{context[:2000]}

Student's Question:
{question}
"""
        result = call_ai(prompt)
        return jsonify({"answer": result})
    except Exception as e:
        return handle_error(e, "Error in chat response")

if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
