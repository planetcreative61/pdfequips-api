import tempfile
import subprocess

def md_text_to_pdf(md_text):
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.md') as temp:
        temp.write(md_text)
        temp_path = temp.name

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.pdf') as temp_pdf:
        pdf_path = temp_pdf.name

    subprocess.run(['mdpdf', temp_path, '-o', pdf_path], check=True)

    return temp_path, pdf_path
