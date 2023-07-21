from io import StringIO
import zipfile
from PyPDF2 import PdfReader
import os
from tempfile import NamedTemporaryFile
import shutil


# pdf to text converter function.
def pdf_to_text(file):
    pdf_reader = PdfReader(file)
    text = StringIO()
    for page in pdf_reader.pages:
        text.write(page.extract_text())
    return text.getvalue()





def pdf_to_text_multiple(files):
    texts = []
    for file in files:
        text = pdf_to_text(file)
        original_filename = file.filename
        base_filename, file_extension = os.path.splitext(original_filename)
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(text)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            new_filename = base_filename + '.txt'
            shutil.move(tmp_file.name, new_filename)
            texts.append((new_filename, os.path.basename(base_filename) + '.txt'))
    zip_file = NamedTemporaryFile(mode='w+b', delete=False, suffix='.zip')
    with zipfile.ZipFile(zip_file, 'w') as zip:
        for text_file, original_filename in texts:
            zip.write(text_file, original_filename)
            os.remove(text_file)
    zip_file.flush()
    os.fsync(zip_file.fileno())
    zip_file.seek(0)
    return zip_file