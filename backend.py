from flask import Flask, request, jsonify
from ai_helper import call_ai

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]
    prompt = f"Summarize this in simple points:\n{text}"
    result = call_ai(prompt)
    return jsonify({"summary": result})


@app.route("/questions", methods=["POST"])
def questions():
    text = request.json["text"]
    prompt = f"Generate 5 easy to medium questions:\n{text}"
    result = call_ai(prompt)
    return jsonify({"questions": result})


@app.route("/chat", methods=["POST"])
def chat():
    text = request.json["text"]
    question = request.json["question"]

    prompt = f"Based on this content:\n{text}\nAnswer:\n{question}"
    result = call_ai(prompt)
    return jsonify({"answer": result})


if __name__ == "_main_":
    app.run(debug=True)