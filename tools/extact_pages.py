from PyPDF2 import PdfReader, PdfWriter
import os
from tempfile import NamedTemporaryFile
import zipfile
import re


def extract_pages(file, selected_pages, merge):
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

    if selected_pages == "all":
        # Extract each page into a new PDF file
        for i, page in enumerate(pdf.pages):
            # Create a new PDF writer
            output = PdfWriter()
            output.add_page(page)

            # Save the output PDF to a new file with the modified filename
            output_file_name = f"{file_name_without_ext}-{i+1}{file_ext}"
            # Remove random characters
            output_file_name = re.sub(r'[^a-zA-Z0-9_-]', '', output_file_name)
            output_file = NamedTemporaryFile(
                suffix='.pdf', delete=False, prefix=output_file_name)
            output.write(output_file)
            output_files.append(output_file.name)
    else:
        # Extract pages based on the selected_pages format
        page_ranges = re.findall(r'\d+(?:-\d+)?', selected_pages)
        for i, page_range in enumerate(page_ranges):
            # Parse the page range
            if '-' in page_range:
                start_page, end_page = map(int, page_range.split('-'))
            else:
                start_page = end_page = int(page_range)

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

    if merge == "true":
        # Merge the extracted PDF files into one PDF file
        merged_output = PdfWriter()
        for output_file_path in output_files:
            with open(output_file_path, 'rb') as output_file:
                pdf_reader = PdfReader(output_file)
                for page in pdf_reader.pages:
                    merged_output.add_page(page)

        # Save the merged PDF to a new file
        merged_output_file_name = f"{file_name_without_ext}-merged{file_ext}"
        # Remove random characters
        merged_output_file_name = re.sub(
            r'[^a-zA-Z0-9_-]', '', merged_output_file_name)
        merged_output_file = NamedTemporaryFile(
            suffix='.pdf', delete=False, prefix=merged_output_file_name)
        merged_output.write(merged_output_file)
        merged_output_file_path = merged_output_file.name

        # Return the merged output file path
        return [merged_output_file_path]

    # If there is only one output file, return the file path
    if len(output_files) == 1:
        return [output_files[0]]

    # If there are multiple output files, create a zip folder
    zip_file_path = NamedTemporaryFile(suffix='.zip', delete=False).name
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for file_path in output_files:
            zip_file.write(file_path, os.path.basename(file_path))

    return [zip_file_path, output_files]
