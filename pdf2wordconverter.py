import io
from werkzeug.datastructures import FileStorage
import os
import tempfile
import subprocess
from flask import send_file, after_this_request
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
    command = f'java -jar /var/www/pdfequips/html/java_programs/pdf-to-word-converter/target/pdf-to-word-converter-1.0-SNAPSHOT.jar "{temp_path}"'
    subprocess.run(command, shell=True, check=True)

    response = send_file(output_file, as_attachment=True, mimetype='application/msword')
    os.remove(output_file)
    os.remove(temp)
    return response




def pdf_to_word_converter_multiple(pdf_files):
    # Create a temporary directory to store the converted files
    temp_dir = tempfile.mkdtemp()

    # Convert each PDF file to Word format
    converted_files = []
    for pdf_file in pdf_files:
        # Save the PDF file with the original name to the temporary directory
        temp_pdf_path = os.path.join(temp_dir, pdf_file.filename)
        pdf_file.save(temp_pdf_path)

        # Extract the filename without extension
        file_name_without_ext = os.path.splitext(os.path.basename(temp_pdf_path))[0]

        # Convert the PDF file to Word using the Java program
        output_dir = '/tmp'
        output_file = os.path.join(output_dir, f'{file_name_without_ext}.docx')
        command = f'java -jar /var/www/pdfequips/html/java_programs/pdf-to-word-converter/target/pdf-to-word-converter-1.0-SNAPSHOT.jar "{temp_pdf_path}"'
        subprocess.run(command, shell=True, check=True)

        # Move the converted Word file to the temporary directory
        temp_word_path = os.path.join(temp_dir, f'{file_name_without_ext}.docx')
        shutil.move(output_file, temp_word_path)

        # Store the path of the converted Word file
        converted_files.append(temp_word_path)

    # Create a zip file containing the converted Word files
    zip_path = os.path.join(temp_dir, 'converted_files.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for word_file in converted_files:
            zip_file.write(word_file, os.path.basename(word_file))

    @after_this_request
    def cleanup(response):
        # Clean up temporary files and directory
        shutil.rmtree(temp_dir)
        return response

    # Return the zip file to the client
    return send_file(zip_path, as_attachment=True, mimetype='application/zip')
