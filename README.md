# HenriPDF

## Description

A project that allows you to concatenate and summarize PDFs with AI. It features a graphical interface for selecting PDFs and viewing the summary. It uses Python, Agno, and Llama 3.3 (or another model of your choice).

## Folder Structure

output : Where concatenations of PDFs will be.
/pdfs : Where you put pdfs.
.env : Put your API key here (Instructions above!).
main.py : File to run.
requirements.txt : File with all libraries to run the file.

## Instructions to use

1. **Make sure you have python 3.9 or newer, and both tkinter and venv modules installed.**

2. **Clone the repository:**
   ```bash
   git init
   git clone 'https://github.com/HenriqueSM0/henri_pdf'

3. **Create a virtual environment:**
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

5. **Create an API key in GROQ:**
   Put it on .env :
   GROQ_KEY_API = 'your_api_key_here'
   
7. **Add PDF files:**
   Place the PDFs you want to process in the pdfs/ folder

8. **Run the application:**
   python main.py
