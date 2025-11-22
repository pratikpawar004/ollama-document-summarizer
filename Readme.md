# 📄 Document Summarizer (Powered by Ollama LLaMA)

A modern, professional web application to **summarize documents** using **local Ollama LLaMA models**. Upload `.txt`, `.md`, or `.pdf` files or paste text directly. The app supports **brief, detailed, or bullet-point summaries**, and displays a **loader while processing**.

---

## 🖥 Features

- Summarizes documents using **Ollama LLaMA** local models  
- Supports **file upload (.txt, .md, .pdf)** or direct text input  
- Multiple summarization styles: **brief, detailed, bullets**  
- Clean and responsive UI 
- **Loader animation** while generating summaries  
- Footer dynamically shows **Ollama status**  

---

## 🚀 Requirements

- Python 3.10+  
- Flask  
- requests  
- python-dotenv  
- PyPDF2 (for PDF extraction)  
- Ollama LLaMA installed and running locally  

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/document-summarizer.git
cd document-summarizer
```
2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Ensure Ollama LLaMA is running locally:**
```bash
ollama run llama3.2
```
Check that your model is running at http://localhost:11434
## 📝 Usage

1. **Run the Flask app**
```bash
python app.py
```
2. **Open your browser and go to:**

     http://127.0.0.1:5000/

3. **Use the UI:**

- Paste text or upload a .txt, .md, or .pdf file

- Select summarization style: brief, detailed, or bullets

- Adjust maximum tokens if needed

4. **Click Summarize**

- The loader will show while generating, and the summary will appear below

## 🗂 File Structure

```
document-summarizer/
│
├── app.py                 # Main Flask app
├── templates/
│   └── index.html         # HTML template
├── static/
│   └── (optional CSS/JS)  # For future enhancements
├──requirements.txt # Python dependencies
└── test.txt  # Sample text file  

```
## ⚠️ Notes
- Ensure Ollama LLaMA is running before using the app

- Maximum input length is 5000 characters

- PDF extraction may not work perfectly for scanned or image PDFs

## 👨‍💻 Author

Pratik Pawar

