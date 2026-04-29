import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:5000"


def summarize(text):
    try:
        res = requests.post(f"{BACKEND_URL}/summarize", json={"text": text})
        return res.json().get("summary", "Error getting summary.")
    except Exception as e:
        return f"Backend error: {str(e)}"
    
def upload_pdf(file):
    try:
        files = {"file": open(file.name, "rb")}
        res = requests.post(f"{BACKEND_URL}/upload_pdf", files=files)
        return res.json().get("text", "Error extracting PDF")
    except Exception as e:
        return str(e)


def questions(text):
    try:
        res = requests.post(f"{BACKEND_URL}/questions", json={"text": text})
        return res.json().get("questions", "Error getting questions.")
    except Exception as e:
        return f"Backend error: {str(e)}"


def mcq(text):
    try:
        res = requests.post(f"{BACKEND_URL}/mcq", json={"text": text})
        return res.json().get("mcq", "Error getting MCQs.")
    except Exception as e:
        return f"Backend error: {str(e)}"


def chat(question, context):
    try:
        res = requests.post(f"{BACKEND_URL}/chat", json={
            "question": question,
            "context": context
        })
        return res.json().get("answer", "Error getting answer.")
    except Exception as e:
        return f"Backend error: {str(e)}"


css = """
.gradio-container {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    min-height: 100vh;
}
textarea, input {
    background: #1e1e2e !important;
    color: #cdd6f4 !important;
    border-radius: 10px !important;
    border: 1px solid #45475a !important;
}
label {
    color: #cdd6f4 !important;
}
button {
    background: linear-gradient(45deg, #7b2ff7, #f107a3) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
"""

with gr.Blocks(css=css, title="Study Genie") as app:
    gr.Markdown("# Study Genie")
    gr.Markdown("### Your AI-powered Study Assistant")

    notes = gr.Textbox(
        label="Paste your study notes here",
        lines=8,
        placeholder="Paste your notes here and click any button below..."
    )
     

    gr.Markdown("### UPLOAD PDF")
    pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
    pdf_btn = gr.Button("Extract PDF Text")

    gr.Markdown("### Summary")
    summary_output = gr.Textbox(lines=5, show_label=False)
    btn_summarize = gr.Button("Summarize")

    gr.Markdown("### Questions")
    questions_output = gr.Textbox(lines=6, show_label=False)
    btn_questions = gr.Button("Generate Questions")

    gr.Markdown("### MCQs")
    mcq_output = gr.Textbox(lines=8, show_label=False)
    btn_mcq = gr.Button("Generate MCQs")

    gr.Markdown("### Chat with your notes")
    chat_q = gr.Textbox(label="Ask a question about your notes")
    chat_btn = gr.Button("Ask AI")
    chat_out = gr.Textbox(label="Answer", lines=4)

    pdf_btn.click(upload_pdf, inputs=pdf_input, outputs=notes)
    btn_summarize.click(summarize, inputs=notes, outputs=summary_output)
    btn_questions.click(questions, inputs=notes, outputs=questions_output)
    btn_mcq.click(mcq, inputs=notes, outputs=mcq_output)
    chat_btn.click(chat, inputs=[chat_q, notes], outputs=chat_out)


if __name__ == "__main__":
    app.launch()
