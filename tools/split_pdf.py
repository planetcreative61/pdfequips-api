from PyPDF2 import PdfReader, PdfWriter
import os
from tempfile import NamedTemporaryFile
import zipfile


"""
    please help me with this function,
    the tmp files should be named with the exact original filename-{i} example: file: test.pdf ranges: [{from: 1: to: 1}, {from: 2, to: 2}]
    output files should be test-1.pdf and test-2.pdf and so on you get the idea.
    also after returning the files the tmp files should be removed.
    as you can see from the output below they still exist after the return
    gitpod /workspace/pdfequips-api (master) $ ls /tmp
    tmp5bfwmsp5  tmp96_b12i_.pdf  tmpktlcmthq.pdf  tmpvezqx9q3.pdf
    gitpod /workspace/pdfequips-api (master) $ 
"""

def split_by_range(file, ranges):
    # Save the file to a temporary folder
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Open the PDF file
    pdf = PdfReader(temp_file.name)

    # Create a list to store the output file paths
    output_files = []

    # Iterate over the ranges
    for range_obj in ranges:
        start_page = range_obj['from']
        end_page = range_obj['to']

        # Create a new PDF writer
        output = PdfWriter()

        # Add the pages within the range to the new PDF writer
        for page_num in range(start_page - 1, end_page):
            # PyPDF2.errors.DeprecationError: reader.getPage(pageNumber) is deprecated and was removed in PyPDF2 3.0.0. Use reader.pages[page_number] instead.
            output.add_page(pdf.pages[page_num])
            # reader.pages[page_number]

        # Save the output PDF to a new file
        output_file = NamedTemporaryFile(suffix='.pdf', delete=False)
        output.write(output_file)
        output_files.append(output_file.name)

    # If there is only one range, return the file path
    if len(ranges) == 1:
        return output_files

    # If there are multiple ranges, create a zip folder
    zip_file_path = NamedTemporaryFile(suffix='.zip', delete=False).name
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for file_path in output_files:
            zip_file.write(file_path, os.path.basename(file_path))

    return zip_file_path


def save_file(file):
    # Create a temporary file to save the uploaded file
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Return the path of the saved file
    return temp_file.name
