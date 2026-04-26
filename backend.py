from flask import Flask, request, jsonify

print("🔥 Backend starting...")

app = Flask(__name__)

# Safe import (VERY IMPORTANT)
try:
    from ai_helper import call_ai
    AI_AVAILABLE = True
    print("✅ AI helper loaded")
except Exception as e:
    print("❌ AI helper failed:", e)
    AI_AVAILABLE = False


@app.route("/")
def home():
    return "Backend is working!"


@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text", "")

    if not AI_AVAILABLE:
        return jsonify({"summary": "AI not working yet"})

    result = call_ai(f"Summarize this:\n{text}")
    return jsonify({"summary": result})


@app.route("/questions", methods=["POST"])
def questions():
    text = request.json.get("text", "")

    if not AI_AVAILABLE:
        return jsonify({"questions": "AI not working yet"})

    result = call_ai(f"Generate 5 questions:\n{text}")
    return jsonify({"questions": result})


@app.route("/mcq", methods=["POST"])
def mcq():
    text = request.json.get("text", "")

    if not AI_AVAILABLE:
        return jsonify({"mcq": "AI not working yet"})

    result = call_ai(f"Generate MCQs:\n{text}")
    return jsonify({"mcq": result})


@app.route("/chat", methods=["POST"])
def chat():
    question = request.json.get("question", "")
    context = request.json.get("context", "")

    if not AI_AVAILABLE:
        return jsonify({"answer": "AI not working yet"})

    result = call_ai(f"Context:\n{context}\n\nQuestion:\n{question}")
    return jsonify({"answer": result})


print("🚀 Starting Flask server...")
app.run(host="127.0.0.1", port=5000)