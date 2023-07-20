from io import StringIO

from PyPDF2 import PdfReader

def pdf_to_text(file):
    pdf_reader = PdfReader(file)
    text = StringIO()
    for page in pdf_reader.pages:
        text.write(page.extract_text())
    return text.getvalue()