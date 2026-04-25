import gradio as gr
import requests

BASE_URL = "http://127.0.0.1:5000"

def summarize(text):
    res = requests.post(f"{BASE_URL}/summarize", json={"text": text})
    return res.json()["summary"]

def generate_questions(text):
    res = requests.post(f"{BASE_URL}/questions", json={"text": text})
    return res.json()["questions"]

def chat(text, question):
    res = requests.post(f"{BASE_URL}/chat", json={
        "text": text,
        "question": question
    })
    return res.json()["answer"]

with gr.Blocks() as app:
    gr.Markdown("# 📚 StudyGenie AI")

    notes = gr.Textbox(label="Paste your notes", lines=10)

    with gr.Row():
        btn1 = gr.Button("Summarize")
        btn2 = gr.Button("Generate Questions")

    summary = gr.Textbox(label="Summary")
    questions = gr.Textbox(label="Questions")

    btn1.click(summarize, inputs=notes, outputs=summary)
    btn2.click(generate_questions, inputs=notes, outputs=questions)

    gr.Markdown("## 💬 Ask Questions")

    user_q = gr.Textbox(label="Your Question")
    answer = gr.Textbox(label="Answer")

    chat_btn = gr.Button("Ask")

    chat_btn.click(chat, inputs=[notes, user_q], outputs=answer)

app.launch()