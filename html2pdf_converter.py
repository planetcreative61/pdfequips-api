from flask import send_file
import os
import tempfile
import subprocess
import zipfile

def html_to_pdf_multiple(html_files):
    # Create a temporary directory for the zip file
    with tempfile.TemporaryDirectory() as tempdir:
        zip_path = os.path.join(tempdir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for html_file in html_files:
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
                    html_file.seek(0)  # Move the file pointer to the beginning
                    temp.write(html_file.read())
                    temp_path = temp.name

                output_dir = tempfile.gettempdir()
                pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".html", ".pdf"))

                subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
                os.remove(temp_path)

                # if not os.path.exists(pdf_file):
                #     return jsonify({"error": "Failed to convert HTML file to PDF"}), 500 # type: ignore

                zipf.write(pdf_file, os.path.relpath(pdf_file, output_dir))
                os.remove(pdf_file)  # Remove the temporary PDF file

        # Return the zip file
        return send_file(zip_path, as_attachment=True, mimetype='application/zip', download_name="converted_files.zip")


"""
    html to pdf should be web to pdf i.e url to pdf!
"""

def html_to_pdf(html_file):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
        html_file.seek(0)  # Move the file pointer to the beginning
        temp.write(html_file.read())
        temp_path = temp.name

    output_dir = tempfile.gettempdir()
    pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".html", ".pdf"))

    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
    os.remove(temp_path)

    # if not os.path.exists(pdf_file):
    #     return jsonify({"error": "Failed to convert HTML file to PDF"}), 500

    response = send_file(pdf_file, as_attachment=True, mimetype='application/pdf')
    os.remove(pdf_file)
    return response
