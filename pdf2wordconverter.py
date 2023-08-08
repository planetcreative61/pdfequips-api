import io
from werkzeug.datastructures import FileStorage
import os
import tempfile
import subprocess
from flask import send_file
import zipfile
import shutil


def pdf_to_word_converter(pdf_file):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
        pdf_file.seek(0)
        temp.write(pdf_file.read())
        temp_path = temp.name

    # Extract filename without extension from temp file path
    file_name_without_ext = os.path.splitext(os.path.basename(temp_path))[0]
    
    output_dir = '/tmp'
    output_file = os.path.join(output_dir, f'{file_name_without_ext}.docx')

    # Use custom Java program for conversion
    # Provide absolute path to jar file
    command = f'java -jar /home/pdfequips/htdocs/pdfequips.com/java_programs/pdf-to-word-converter/target/pdf-to-word-converter-1.0-SNAPSHOT.jar "{temp_path}"'
    subprocess.run(command, shell=True, check=True)

    response = send_file(output_file, as_attachment=True, mimetype='application/msword')
    os.remove(output_file)
    os.remove(temp_path)
    return response







# this function is working fine, however the generated files should be named the same names as the orinal filenames not just random names, i mean the original uploaded file names.
# also the pdf files should be removed along with the word files after adding the word files to the zip folder

def pdf_to_word_converter_multiple(pdf_files):
    word_files = []
    for pdf_file in pdf_files:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            pdf_file.seek(0)
            temp.write(pdf_file.read())
            temp_path = temp.name

        # Extract filename without extension from temp file path
        file_name_without_ext = os.path.splitext(os.path.basename(temp_path))[0]
        output_dir = '/tmp'
        output_file = os.path.join(output_dir, f'{file_name_without_ext}.docx')

        # Use custom Java program for conversion
        command = f'java -jar /home/pdfequips/htdocs/pdfequips.com/java_programs/pdf-to-word-converter/target/pdf-to-word-converter-1.0-SNAPSHOT.jar "{temp_path}"'
        subprocess.run(command, shell=True, check=True)

        word_files.append(output_file)

    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for word_file in word_files:
            zipf.write(word_file, os.path.basename(word_file))
            # Delete the Word file after adding it to the zip
            os.remove(word_file)
            os.remove(temp_path)

    # Set the buffer's position to the beginning of the file
    zip_buffer.seek(0)

    # Return the zip file
    return send_file(zip_buffer, as_attachment=True, download_name="converted_files.zip", mimetype="application/zip")