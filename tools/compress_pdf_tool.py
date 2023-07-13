import os
import tempfile


def compress_pdf(pdf_file):
    # Create a temporary file to store the compressed PDF
    compressed_pdf = tempfile.NamedTemporaryFile(delete=False)

    # Command to run Ghostscript
    command = f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile={compressed_pdf.name} {pdf_file}'

    # Run Ghostscript
    os.system(command)

    # Get the filename of the compressed PDF
    compressed_pdf_filename = compressed_pdf.name

    # Close and delete the temporary file
    compressed_pdf.close()

    # Return the compressed PDF file name
    return compressed_pdf_filename