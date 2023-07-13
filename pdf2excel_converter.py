from tabula.io import read_pdf
import tempfile
import os
import pandas as pd
from flask import send_file, jsonify
import zipfile


"""
    okay this function is working, but now i want another function called pdf_to_excel_multiple
    which takes a list which is: request.files.getlist("files")
    it should loop through all pdf files convert them and return them all in a zip file for download.
"""

def pdf_to_excel(files):
    for pdf_file in files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            pdf_file.seek(0)
            temp.write(pdf_file.read())
            temp_path = temp.name

        output_dir = tempfile.gettempdir()
        excel_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".pdf", ".xlsx"))

        # Convert PDF to Excel
        dfs = read_pdf(temp_path, pages="all", multiple_tables=True)

        # Concatenate data frames into a single data frame
        combined_df = pd.concat(dfs, ignore_index=True)

        # Save the combined data frame to an Excel file
        combined_df.to_excel(excel_file, index=False)

        if not os.path.exists(excel_file):
            return jsonify({"error": "Failed to convert PDF file to Excel"}), 500

        response = send_file(excel_file, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        os.remove(excel_file)
        return response



"""
    please meke the funciton to store the zip file in a /tmp folder. right now it's sotring it in the
    current working directory.
"""
import os
import tempfile
import zipfile
from flask import send_file, jsonify

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
        excel_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".pdf", ".xlsx"))
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
