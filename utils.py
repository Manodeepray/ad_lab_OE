import os
from PyPDF2 import PdfReader
import io

def get_resume_content(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        print(f"Number of pages: {num_pages}")

        text = reader.pages[0].extract_text() if num_pages > 0 else ""
        print(text)

    return text

def get_resume_from_bytes(uploaded_pdf) -> str:
    pdf_reader = PdfReader(io.BytesIO(uploaded_pdf.getbuffer()))

    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n\n"
        
    return text
if __name__ == "__main__":
    pdf_path = "./uploaded_resumes/manodeep_resume_2025_march1.pdf"
    
    if pdf_path:
        resume_text = get_resume_from_bytes(pdf_path)
    else:
        print(f"File {pdf_path} not found!")
