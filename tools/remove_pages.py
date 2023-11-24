from PyPDF2 import PdfReader, PdfWriter
import os
from tempfile import NamedTemporaryFile
import re

def remove_pages(file, selected_pages):
    # Save the file to a temporary folder
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Open the PDF file
    pdf = PdfReader(temp_file.name)

    # Create a new PDF writer
    output = PdfWriter()

    # Parse the selected_pages string to get a list of pages to be removed
    pages_to_remove = set()
    for range_str in selected_pages.split(','):
        if '-' in range_str:
            start, end = map(int, range_str.split('-'))
            pages_to_remove.update(range(start - 1, end))  # Subtract 1 because pages in PDF are 0-indexed
        else:
            pages_to_remove.add(int(range_str) - 1)  # Subtract 1 because pages in PDF are 0-indexed

    # Add the pages that are not in the pages_to_remove set to the new PDF writer
    for i, page in enumerate(pdf.pages):
        if i not in pages_to_remove:
            output.add_page(page)

    # Save the output PDF to a new file
    output_file = NamedTemporaryFile(suffix='.pdf', delete=False)
    output.write(output_file)

    # Remove the original file
    os.remove(temp_file.name)

    # Return the path to the new file
    return output_file.name
