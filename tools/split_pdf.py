from PyPDF2 import PdfReader, PdfWriter
import os
from tempfile import NamedTemporaryFile
import zipfile
import re


def split_by_range(file, ranges):
    # Save the file to a temporary folder
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Extract the filename and extension from the original file path
    file_name = os.path.basename(file.filename)
    file_name_without_ext, file_ext = os.path.splitext(file_name)

    # Open the PDF file
    pdf = PdfReader(temp_file.name)

    # Create a list to store the output file paths
    output_files = []

    # Iterate over the ranges
    for i, range_obj in enumerate(ranges):
        start_page = range_obj['from']
        end_page = range_obj['to']

        # Create a new PDF writer
        output = PdfWriter()

        # Add the pages within the range to the new PDF writer
        for page_num in range(start_page - 1, end_page):
            output.add_page(pdf.pages[page_num])

        # Save the output PDF to a new file with the modified filename
        output_file_name = f"{file_name_without_ext}-{i+1}{file_ext}"
        # Remove random characters
        output_file_name = re.sub(r'[^a-zA-Z0-9_-]', '', output_file_name)
        output_file = NamedTemporaryFile(
            suffix='.pdf', delete=False, prefix=output_file_name)
        output.write(output_file)
        output_files.append(output_file.name)

    # If there is only one range, return the file paths
    if len(ranges) == 1:
        return [output_files]

    # If there are multiple ranges, create a zip folder
    zip_file_path = NamedTemporaryFile(suffix='.zip', delete=False).name
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for file_path in output_files:
            zip_file.write(file_path, os.path.basename(file_path))

    return [zip_file_path, output_files]
