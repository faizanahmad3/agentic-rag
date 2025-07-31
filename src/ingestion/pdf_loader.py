import os
from pypdf import PdfReader

def load_pdf(file_path: str):
    """
    Extract text from each page of a PDF file.
    Returns list of dicts: file_name, page_number, text.
    """
    reader = PdfReader(file_path)
    file_name = os.path.basename(file_path)
    pages_data = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            pages_data.append({
                "file_name": file_name,
                "page_number": page_num,
                "text": text
            })

    return pages_data
