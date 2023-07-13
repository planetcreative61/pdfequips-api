from io import BytesIO
import os
import tempfile

from PyPDF2 import PdfMerger


def merge_pdfs(pdf_files):

    # Check if pdf_files is a list of PDF files
    if not isinstance(pdf_files, list):
        raise TypeError("pdf_files must be a list of PDF file paths")

    # Check if the PDF files exist
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"No such file or directory: '{pdf_file}'")

    # Create a temporary merged PDF file
    temp_merged_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_merged_pdf.close()

    # Initialize PdfMerger
    merger = PdfMerger()

    # Merge the PDF files
    for pdf_file in pdf_files:
        merger.append(pdf_file)

    # Write the merged PDF to the temporary file
    with open(temp_merged_pdf.name, "wb") as f:
        merger.write(f)

    # Read the merged PDF file and return
    with open(temp_merged_pdf.name, "rb") as f:
        merged_pdf = BytesIO(f.read())

    # Delete temporary merged PDF file
    os.unlink(temp_merged_pdf.name)

    return merged_pdf
