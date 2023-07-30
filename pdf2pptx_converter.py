import os
import tempfile
from flask import send_file, after_this_request
from werkzeug.datastructures import FileStorage
from pdf2docx import Converter
import zipfile
from io import BytesIO
import shutil


def pdf_to_pptx(file_storage: FileStorage):
    # Create a temporary file and save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        file_storage.save(temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    # Create a temporary file for the output pptx
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as temp_pptx:
        temp_pptx_path = temp_pptx.name

    # Convert the PDF to PPTX using the pdf2pptx library
    converter = Converter(temp_pdf_path)
    converter.convert(temp_pptx_path)
    converter.close()
    response = send_file(temp_pptx_path, as_attachment=True, download_name='converted.pptx',
                         mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'close'
    # Delete the temporary PDF file

    @after_this_request
    def remove_file(response):
        os.remove(temp_pptx.name)
        os.remove(temp_pdf.name)
        return response

    # Return the converted PPTX file using Flask's send_file
    return response


def pdf_to_pptx_multiple(files):
    # Create a temporary folder to store the converted PPTX files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Iterate through the list of files and convert them to PPTX
        for file_storage in files:
            # Create a temporary file and save the uploaded file
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
                file_storage.save(temp_pdf.name)
                temp_pdf_path = temp_pdf.name

            # Create a temporary file for the output PPTX
            with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as temp_pptx:
                temp_pptx_path = temp_pptx.name

            # Convert the PDF to PPTX using the pdf2docx library
            converter = Converter(temp_pdf_path)
            converter.convert(temp_pptx_path, pptx=True)
            converter.close()

            # Delete the temporary PDF file
            os.remove(temp_pdf_path)

            # Get the filename without the extension
            filename_without_ext, _ = os.path.splitext(file_storage.filename)

            # Move the converted PPTX file to the temporary folder with the new name
            shutil.move(temp_pptx_path, os.path.join(
                temp_dir, f'{filename_without_ext}.pptx'))

        # Create a zip file containing the converted PPTX files
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for file_name in os.listdir(temp_dir):
                zipf.write(os.path.join(temp_dir, file_name), file_name)

        # Set the buffer's file pointer to the beginning of the file
        zip_buffer.seek(0)
        response = send_file(zip_buffer, as_attachment=True,
                             download_name='converted_files.zip', mimetype='application/zip')
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Connection'] = 'close'

        # Return the zip file for download
        return response
