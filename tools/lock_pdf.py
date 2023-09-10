from flask import send_file
from io import BytesIO
import zipfile
from PyPDF2 import PdfReader, PdfWriter


def lock_pdf_file(file, password):
    pdf_reader = PdfReader(file)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(user_password=password, owner_pwd=None, use_128bit=True)

    output_buffer = BytesIO()
    pdf_writer.write(output_buffer)
    locked_pdf = output_buffer.getvalue()
    output_buffer.close()

    return locked_pdf


def lock_multiple_pdf_files(files, password):
    zip_buffer = BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)

    for file in files:
        locked_pdf = lock_pdf_file(file, password)
        locked_filename = f"{file.filename.split('.')[0]}_locked.pdf"
        zip_file.writestr(locked_filename, locked_pdf)

    zip_file.close()

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='locked_files.zip')
