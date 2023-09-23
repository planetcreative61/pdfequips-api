import os
import zipfile
import shutil
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from tempfile import NamedTemporaryFile


def rotate_pdf(file, angle):
    # Save the FileStorage to a temporary file
    with NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file)
        file_path = temp_file.name

    # Create a PDF reader object
    reader = PdfReader(file_path)
    writer = PdfWriter()

    # Rotate each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.rotate(angle)
        writer.add_page(page)

    # Write out the rotated PDF to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".pdf") as out_file:
        writer.write(out_file)

    return out_file.name


"""
    thank you very much the function is working as i wanted it to be, but i want to return the tmp_directory as well to the function caller
    so that i can delete it letter.
    this is how i'm calling the function, the tmp folder however is not deleted but the zip folder is for now,
    zip_file = rotate_pdf_multiple(files=files, angles=angles)
            response = send_file(zip_file, mimetype='application/zip',
                                 as_attachment=True, download_name='output.zip', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(zip_file)
                return response

            return response
"""


def rotate_pdf_multiple(files, angles):
    # Create a temporary directory to store the rotated files
    temp_directory = tempfile.mkdtemp()

    # Rotate each file
    rotated_files = []
    for file, angle_dict in zip(files, angles):
        # Get the original file name
        original_filename = file.filename

        # Extract the rotation angle from the angle dictionary
        angle = angle_dict['value']

        # Rotate the PDF file
        rotated_filename = rotate_pdf(file, angle)

        # Move the rotated file to the temporary directory
        rotated_file_path = os.path.join(temp_directory, original_filename)
        shutil.move(rotated_filename, rotated_file_path)

        # Store the rotated file path
        rotated_files.append(rotated_file_path)

    # Create a zip file to store the rotated files
    zip_filename = os.path.join(temp_directory, "rotated_files.zip")
    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        # Add each rotated file to the zip file
        for rotated_file in rotated_files:
            zip_file.write(rotated_file, os.path.basename(rotated_file))

    return zip_filename, temp_directory
