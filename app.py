import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:5000"

# -------- FUNCTIONS --------

def summarize(text):
    try:
        res = requests.post(f"{BACKEND_URL}/summarize", json={"text": text})
        return res.json().get("summary", "Error")
    except:
        return "Backend error"

def questions(text):
    try:
        res = requests.post(f"{BACKEND_URL}/questions", json={"text": text})
        return res.json().get("questions", "Error")
    except:
        return "Backend error"

def mcq(text):
    try:
        res = requests.post(f"{BACKEND_URL}/mcq", json={"text": text})
        return res.json().get("mcq", "Error")
    except:
        return "Backend error"

def chat(q, context):
    try:
        res = requests.post(f"{BACKEND_URL}/chat", json={
            "question": q,
            "context": context
        })
        return res.json().get("answer", "Error")
    except:
        return "Backend error"


# -------- FINAL CSS (CORRECT TARGET) --------
css = """
/* Background stays same */
.gradio-container {
    background: url('https://i.ibb.co/gZ182gSN/Gemini-Generated-Image-97cqnk97cqnk97cq.png') no-repeat center center fixed;
    background-size: cover;
}

/* 🔥 FIX BLACK STRIP (MAIN CONTAINER) */
.gr-box {
    background: #ffe6f0 !important;
    border: none !important;
    box-shadow: none !important;
}

/* ALSO FIX INNER WRAPPER */
.gr-box > div {
    background: #ffe6f0 !important;
}

/* TEXTBOX AREA */
textarea, input {
    background: #fff0f5 !important;
    color: black !important;
    border-radius: 10px !important;
}

/* LABEL TEXT */
label {
    color: black !important;
}

/* BUTTONS */
button {
    background: linear-gradient(45deg, #7b2ff7, #f107a3) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold;
}

/* GENERAL TEXT */
body, h1, h2, h3, p {
    color: black !important;
}
"""

# -------- UI --------
with gr.Blocks(css=css) as app:

    gr.Markdown("#  Study Genie  ")
    gr.Markdown("### Smart Study Assistant ")

    notes = gr.Textbox(label="📄 Paste your notes", lines=8)

    with gr.Row():
        btn1 = gr.Button("✨ Summarize")
        btn2 = gr.Button("❓ Questions")
        btn3 = gr.Button("🎯 MCQs")

    gr.Markdown("### 📌 Summary")
    summary_output = gr.Textbox(lines=5, show_label=False)

    gr.Markdown("### ❓ Questions")
    questions_output = gr.Textbox(lines=5, show_label=False)

    gr.Markdown("### 🎯 MCQs")
    mcq_output = gr.Textbox(lines=5, show_label=False)

    gr.Markdown("### 💬 Ask from your notes")

    chat_q = gr.Textbox(label="Ask a question")
    chat_btn = gr.Button("💬 Ask AI")
    chat_out = gr.Textbox(show_label=False)

    btn1.click(summarize, inputs=notes, outputs=summary_output)
    btn2.click(questions, inputs=notes, outputs=questions_output)
    btn3.click(mcq, inputs=notes, outputs=mcq_output)
    chat_btn.click(chat, inputs=[chat_q, notes], outputs=chat_out)

app.launch()