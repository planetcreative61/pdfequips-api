import os
import tempfile
import subprocess
from flask import send_file
import zipfile


def excel_to_pdf(excel_files):
    for excel_file in excel_files:
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp:
            excel_file.seek(0)  # Move the file pointer to the beginning
            temp.write(excel_file.read())
            temp_path = temp.name

        output_dir = tempfile.gettempdir()
        pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".xlsx", ".pdf"))

        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
        os.remove(temp_path)

        # if not os.path.exists(pdf_file):
        #     return jsonify({"error": "Failed to convert Excel file to PDF"}), 500

        response = send_file(pdf_file, as_attachment=True, mimetype='application/pdf')
        os.remove(pdf_file)
        return response



def excel_to_pdf_multiple(excel_files):
    # Create a temporary directory for the zip file
    with tempfile.TemporaryDirectory() as tempdir:
        zip_path = os.path.join(tempdir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for excel_file in excel_files:
                with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp:
                    excel_file.seek(0)  # Move the file pointer to the beginning
                    temp.write(excel_file.read())
                    temp_path = temp.name

                original_name = os.path.splitext(os.path.basename(temp_path))[0]
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_temp:
                    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", tempfile.gettempdir()], stdout=pdf_temp)

                    # if not os.path.exists(pdf_file):
                    #     return jsonify({"error": "Failed to convert Excel file to PDF"}), 500 # type: ignore

                    zipf.write(pdf_temp.name, original_name + ".pdf")
                    os.remove(temp_path)  # Remove the temporary Excel file
                    os.remove(pdf_temp.name)  # Remove the temporary PDF file

        # Return the zip file
        return send_file(zip_path, as_attachment=True, mimetype='application/zip', download_name="converted_files.zip")
