from flask import Flask, request, jsonify
from flask_cors import CORS

print("Backend starting...")

app = Flask(__name__)
CORS(app)

try:
    from ai_helper import call_ai
    AI_AVAILABLE = True
    print("AI helper loaded successfully")
except Exception as e:
    print("AI helper failed to load:", e)
    AI_AVAILABLE = False


@app.route("/")
def home():
    return "Study Genie Backend is running!"


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        text = request.json.get("text", "").strip()
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
        return jsonify({"summary": f"Error: {str(e)}"})


@app.route("/questions", methods=["POST"])
def questions():
    try:
        text = request.json.get("text", "").strip()
        if not text:
            return jsonify({"questions": "Please provide some notes to generate questions from."})
        if not AI_AVAILABLE:
            return jsonify({"questions": "AI is not available. Check your API key."})

        prompt = f"""Read the following study notes and generate exactly 7 study questions.
Number each question (1. 2. 3. etc.).
Make them clear and useful for a student to test their understanding.

Notes:
{text[:3000]}
"""
        result = call_ai(prompt)
        return jsonify({"questions": result})
    except Exception as e:
        return jsonify({"questions": f"Error: {str(e)}"})


@app.route("/mcq", methods=["POST"])
def mcq():
    try:
        text = request.json.get("text", "").strip()
        if not text:
            return jsonify({"mcq": "Please provide some notes to generate MCQs from."})
        if not AI_AVAILABLE:
            return jsonify({"mcq": "AI is not available. Check your API key."})

        prompt = f"""Generate 5 multiple choice questions (MCQs) from the following study notes.

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
        return jsonify({"mcq": f"Error: {str(e)}"})


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
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
