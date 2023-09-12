import uuid
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
    zip_filename = f"/tmp/{uuid.uuid4()}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            locked_pdf = lock_pdf_file(file, password)
            locked_filename = f"{file.filename.split('.')[0]}_locked.pdf"
            zip_file.writestr(locked_filename, locked_pdf)

    return zip_filename
