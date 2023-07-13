import os
import tempfile
import subprocess
from flask import send_file
import zipfile
import shutil

"""
    i want another function called pdf_to_pptx which takes a pdf file.
    and it should convert it the same approach i.e soffice.
    and return for download.
    i'm then calling the pdf_to_pptx function and passing pdf_files[0] to it which is 
    files = request.files.getlist('files')
"""
def pdf_to_word_converter(pdf_file):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
        pdf_file.seek(0)
        temp.write(pdf_file.read())
        temp_path = temp.name

    output_dir = tempfile.gettempdir()
    output_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".pdf", ".docx"))

    # Use soffice for conversion
    command = f'soffice --infilter="writer_pdf_import" --convert-to docx --outdir "{output_dir}" "{temp_path}"'
    subprocess.run(command, shell=True, check=True)

    response = send_file(output_file, as_attachment=True, mimetype='application/msword')
    os.remove(output_file)
    os.remove(temp_path)
    return response






from werkzeug.datastructures import FileStorage
def pdf_to_word(file_storage: FileStorage):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
        file_storage.save(temp.name)
        temp_path = temp.name

    output_dir = tempfile.gettempdir()
    output_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".pdf", ".docx"))

    command = f'soffice --infilter="writer_pdf_import" --convert-to docx --outdir "{output_dir}" "{temp_path}"'
    subprocess.run(command, shell=True, check=True)

    os.remove(temp_path)  # Delete the temporary PDF file
    return output_file



import io
"""
    please update this funciton, and make it change the stored word file names to be the same as
    the original uploaded pdf files.
    not just random names generated.
"""
def pdf_to_word_converter_multiple(pdf_files):
    # Convert PDF files to Word files
    word_files = [pdf_to_word(pdf_file) for pdf_file in pdf_files]

    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for word_file in word_files:
            zipf.write(word_file, os.path.basename(word_file))
            os.remove(word_file)  # Delete the Word file after adding it to the zip

    # Set the buffer's position to the beginning of the file
    zip_buffer.seek(0)

    # Return the zip file
    return send_file(zip_buffer, as_attachment=True, download_name="converted_files.zip", mimetype="application/zip")
