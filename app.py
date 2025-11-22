import os
import io
import traceback
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import requests
import json

# Flask setup
ALLOWED_EXTENSIONS = {"txt", "md", "pdf"}
MAX_INPUT_CHARS = 5000
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama local endpoint
MODEL = "llama3.2"

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_stream) -> str:
    try:
        reader = PdfReader(file_stream)
        texts = []
        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                texts.append(txt)
        return "\n\n".join(texts)
    except Exception:
        return ""

def read_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext in ('txt', 'md'):
        content = file_storage.stream.read().decode('utf-8', errors='ignore')
        return content
    if ext == 'pdf':
        file_stream = io.BytesIO(file_storage.stream.read())
        return extract_text_from_pdf(file_stream)
    return ""

def build_prompt(text: str, style: str) -> str:
    base = "You are a helpful assistant that summarizes documents."
    if style == 'brief':
        instr = "Provide a concise summary in 1-2 sentences highlighting the main idea and conclusions."
    elif style == 'detailed':
        instr = "Provide a detailed summary in a few paragraphs covering the key points and conclusions."
    else:
        instr = "Provide a bullet-point summary (3-10 items) capturing the main ideas and takeaways."
    prompt = f"{base}\n{instr}\n\nDOCUMENT START:\n{text[:4000]}\n\nDOCUMENT END:\nPlease write the summary now."
    return prompt

def call_ollama(prompt: str) -> str:
    """
    Calls Ollama local API with streaming and returns the full response.
    """
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": MODEL, "prompt": prompt},
            stream=True
        )

        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        output += data["response"]
                except json.JSONDecodeError:
                    continue

        if not output:
            return "⚠️ No response from Ollama. Please check if the model is running."

        return output

    except Exception as e:
        return f"⚠️ Error calling Ollama: {str(e)}\n{traceback.format_exc()}"

def check_ollama_status() -> str:
    """
    Checks if the Ollama model is running by sending a small test prompt.
    """
    try:
        test_prompt = {"model": MODEL, "prompt": "Hello"}
        response = requests.post(OLLAMA_API_URL, json=test_prompt, timeout=2)
        if response.ok:
            return "Powered by Ollama LLaMA ✅"
        else:
            return "Powered by Ollama LLaMA ⚠️ (not responding)"
    except Exception:
        return "Powered by Ollama LLaMA ⚠️ (not running)"

# Routes
@app.route('/', methods=['GET'])
def index():
    ollama_status = check_ollama_status()
    return render_template(
        'index.html',
        summary=None,
        input_text=None,
        style='brief',
        max_tokens=300,
        debug=None,
        ollama_status=ollama_status
    )

@app.route('/summarize', methods=['POST'])
def summarize():
    input_text = (request.form.get('input_text') or '').strip()
    uploaded = request.files.get('file')
    style = request.form.get('style') or 'brief'

    if not input_text and (not uploaded or uploaded.filename == ''):
        flash('Please provide text or upload a file to summarize.')
        return redirect(url_for('index'))

    file_text = ''
    if uploaded and uploaded.filename != '':
        if not allowed_file(uploaded.filename):
            flash('Unsupported file type. Allowed: .txt, .md, .pdf')
            return redirect(url_for('index'))
        file_text = read_uploaded_file(uploaded)

    source_text = file_text if len(file_text) > len(input_text) else input_text

    if len(source_text) > MAX_INPUT_CHARS:
        flash(f'Input too long ({len(source_text)} chars). Limit is {MAX_INPUT_CHARS}.')
        ollama_status = check_ollama_status()
        return render_template('index.html', summary=None, input_text=source_text[:2000], style=style, max_tokens=300, debug=None, ollama_status=ollama_status)

    prompt = build_prompt(source_text, style)
    summary = call_ollama(prompt)
    ollama_status = check_ollama_status()

    return render_template('index.html', summary=summary, input_text=source_text, style=style, max_tokens=300, debug=None, ollama_status=ollama_status)


if __name__ == '__main__':
    app.run(debug=True)
