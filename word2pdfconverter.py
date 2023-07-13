import os
import tempfile
import subprocess
from flask import send_file, jsonify
import zipfile

"""
this function is converting 
"""

def word_to_pdf(word_files):
    for word_file in word_files:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp:
            word_file.seek(0)  # Move the file pointer to the beginning
            temp.write(word_file.read())
            temp_path = temp.name

        output_dir = tempfile.gettempdir()
        pdf_file = os.path.join(output_dir, os.path.basename(temp_path).replace(".docx", ".pdf"))

        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
        os.remove(temp_path)

        if not os.path.exists(pdf_file):
            return jsonify({"error": "Failed to convert Word file to PDF"}), 500

        response = send_file(pdf_file, as_attachment=True, mimetype='application/pdf')
        os.remove(pdf_file)
        return response



"""
    this function is working fine, but the file names in the generated zip should not be random names.
    they should be the same as the original file names.
    for example files: abc.docx, xyz.docx, then output file names in the zip folder should be abc.pdf and xyz.pdf and so on.
"""
def word_to_pdf_multiple(word_files):
    # Create a temporary directory for the zip file
    with tempfile.TemporaryDirectory() as tempdir:
        zip_path = os.path.join(tempdir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for word_file in word_files:
                file_name = word_file.filename
                temp_path = os.path.join(tempdir, file_name)
                with open(temp_path, 'wb') as f:
                    word_file.seek(0)  # Move the file pointer to the beginning
                    f.write(word_file.read())        

                output_dir = tempfile.gettempdir()
                pdf_file_name = os.path.basename(temp_path).replace(".docx", ".pdf")
                pdf_file = os.path.join(output_dir, pdf_file_name)

                subprocess.run(["soffice", "--headless", "--convert-to", "pdf", temp_path, "--outdir", output_dir])
                os.remove(temp_path)

                # Write the PDF file to the zip file with the same filename
                zipf.write(pdf_file, pdf_file_name)
                os.remove(pdf_file)  # Remove the temporary PDF file

        # Return the zip file
        return send_file(zip_path, as_attachment=True, mimetype='application/zip', 
                         download_name="converted_files.zip")