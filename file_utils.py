import fitz  # PyMuPDF
import pandas as pd
from io import BytesIO
import os

FILE_STORAGE_DIR = "uploaded_files"

# Ensure the file storage directory exists
os.makedirs(FILE_STORAGE_DIR, exist_ok=True)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to process other file types (example with CSV and TXT)
def process_file(file, file_type):
    file_content = file.read()
    file_name = file.name
    file_path = os.path.join(FILE_STORAGE_DIR, file_name)

    # Save the file to disk
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Process based on file type
    if file_type == 'application/pdf':
        text = extract_text_from_pdf(BytesIO(file_content))
        return {"type": "pdf", "text": text}
    elif file_type == 'text/csv':
        df = pd.read_csv(BytesIO(file_content))
        return {"type": "csv", "data": df}
    elif file_type == 'text/plain':
        content = file_content.decode("utf-8")
        return {"type": "text", "content": content}
    return None
