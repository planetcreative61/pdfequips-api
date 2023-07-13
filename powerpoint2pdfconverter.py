import os
import tempfile
import subprocess
from flask import send_file, jsonify
import zipfile


"""
    i want another funciton similar to the blow one, called pdf_to_excel that uses similar approach to convert
    from pdf to excel it's beign called like on my flask app this:
    files = request.files.getlist("files")
        return pdf_to_excel(files)
"""
def ppt_to_pdf(ppt_files):
    for ppt_file in ppt_files:
        with tempfile.NamedTemporaryFile(suffix=".ppt", delete=False) as temp:
            ppt_file.seek(0)  # Move the file pointer to the beginning
            temp.write(ppt_file.read())
            temp_path = temp.name

        output_dir = tempfile.gettempdir()
        pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".ppt", ".pdf"))

        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
        os.remove(temp_path)

        if not os.path.exists(pdf_file):
            return jsonify({"error": "Failed to convert PowerPoint file to PDF"}), 500

        response = send_file(pdf_file, as_attachment=True, mimetype='application/pdf')
        os.remove(pdf_file)
        return response


def ppt_to_pdf_multiple(ppt_files):
    # Create a temporary directory for the zip file
    with tempfile.TemporaryDirectory() as tempdir:
        zip_path = os.path.join(tempdir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for ppt_file in ppt_files:
                with tempfile.NamedTemporaryFile(suffix=".ppt", delete=False) as temp:
                    ppt_file.seek(0)  # Move the file pointer to the beginning
                    temp.write(ppt_file.read())
                    temp_path = temp.name

                output_dir = tempfile.gettempdir()
                pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".ppt", ".pdf"))

                subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
                os.remove(temp_path)

                # Get the original file name without the extension
                original_file_name = os.path.splitext(os.path.basename(ppt_file.filename))[0]

                # Write the PDF file to the zip file with the original file name
                pdf_filename = original_file_name + ".pdf"
                zipf.write(pdf_file, pdf_filename)

                os.remove(pdf_file)  # Remove the temporary PDF file

        # Return the zip file
        return send_file(zip_path, as_attachment=True, mimetype='application/zip', download_name="converted_files.zip")