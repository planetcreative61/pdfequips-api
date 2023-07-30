from tabula.io import read_pdf
import tempfile
import os
import pandas as pd
from flask import send_file, jsonify, after_this_request
import zipfile
from werkzeug.utils import secure_filename
import shutil


"""
    i want to create another function similar to this called pdf_to_excel_multiple which takes files
    and it works the same way, but it converts all files and return them for the user in a zip folder for download.
    note that the files in the zip folder should be named the same names as the original file names, but with the excel extension instead of .pdf extension.
    also the function should remove all the files used, and the converted files after the request using: after_this_request
    please give me full solutiotion code
"""


def pdf_to_excel(files):
    for pdf_file in files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            pdf_file.seek(0)
            temp.write(pdf_file.read())
            temp_path = temp.name

        output_dir = tempfile.gettempdir()
        excel_file = os.path.join(output_dir, os.path.basename(
            temp_path).replace(".pdf", ".xlsx"))

        # Convert PDF to Excel
        dfs = read_pdf(temp_path, pages="all", multiple_tables=True)

        # Concatenate data frames into a single data frame
        combined_df = pd.concat(dfs, ignore_index=True)

        # Save the combined data frame to an Excel file
        combined_df.to_excel(excel_file, index=False)

        if not os.path.exists(excel_file):
            return jsonify({"error": "Failed to convert PDF file to Excel"}), 500

        response = send_file(excel_file, as_attachment=True,
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        @after_this_request
        def remove_file(request):
            os.remove(excel_file)
            os.remove(temp_path)
            return request
        return response


"""
    the function is working fine, but the tmp dir output_dir is not removed after the request
"""


def pdf_to_excel_multiple(files):
    output_dir = tempfile.mkdtemp()

    zip_filename = f'{output_dir}/converted_files.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')

    for pdf_file in files:
        filename = secure_filename(pdf_file.filename)
        temp_path = f'{output_dir}/{filename}'
        pdf_file.save(temp_path)

        excel_filename = filename.replace('.pdf', '.xlsx')
        excel_path = f'{output_dir}/{excel_filename}'

        dfs = read_pdf(temp_path, pages='all', multiple_tables=True)
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.to_excel(excel_path, index=False)

        zip_file.write(excel_path, excel_filename)

        os.remove(temp_path)
        os.remove(excel_path)

    zip_file.close()

    response = send_file(zip_filename, as_attachment=True,
                         mimetype='application/zip')

    @after_this_request
    def remove_zip(response):
        shutil.rmtree(output_dir)
        return response

    return response


"""
def pdf_to_excel_multiple(files):
    # Create a temporary directory to store the Excel files
    output_dir = os.path.abspath("/tmp")  # Set the output directory to /tmp

    # Initialize an empty list to store the Excel file paths
    excel_files = []

    # Loop through all the PDF files
    for pdf_file in files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            pdf_file.seek(0)
            temp.write(pdf_file.read())
            temp_path = temp.name

        # Convert PDF to Excel
        dfs = read_pdf(temp_path, pages="all", multiple_tables=True)

        # Concatenate data frames into a single data frame
        combined_df = pd.concat(dfs, ignore_index=True)

        # Save the combined data frame to an Excel file
        excel_file = os.path.join(output_dir, os.path.basename(
            temp_path).replace(".pdf", ".xlsx"))
        combined_df.to_excel(excel_file, index=False)

        # Add the Excel file path to the list
        excel_files.append(excel_file)

        if not os.path.exists(excel_file):
            return jsonify({"error": "Failed to convert PDF file to Excel"}), 500

    # Create a zip archive containing all the Excel files
    zip_filename = "converted_files.zip"
    with zipfile.ZipFile(zip_filename, mode="w") as zipf:
        for excel_file in excel_files:
            zipf.write(excel_file, os.path.relpath(excel_file, output_dir))

    # Return the zip file for download
    return send_file(zip_filename, mimetype='application/zip', as_attachment=True, download_name="converted_files.zip")
"""
