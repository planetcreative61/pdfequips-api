import subprocess
from flask import jsonify, send_file
import io
import tempfile
import os


def pdf_to_pdfa(input_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file_path = os.path.join(temp_dir, 'input.pdf')
        output_file_path = os.path.join(temp_dir, 'output.pdf')

        # Save the FileStorage object to a temporary file
        with open(input_file_path, 'wb') as temp_input_file:
            temp_input_file.write(input_file.read())

        try:
            gs_command = [
                'gs',
                '-dPDFA',
                '-dBATCH',
                '-dNOPAUSE',
                '-dUseCIEColor',
                '-sProcessColorModel=DeviceCMYK',
                '-sDEVICE=pdfwrite',
                '-sPDFACompatibilityPolicy=1',
                f'-sOutputFile={output_file_path}',
                input_file_path
            ]
            subprocess.run(gs_command, check=True)

        except subprocess.CalledProcessError:
            return jsonify({"error": "Conversion to PDF/A failed"}), 400

        with open(output_file_path, 'rb') as pdfa_file:
            pdfa_bytes = io.BytesIO(pdfa_file.read())

        pdfa_bytes.seek(0)

        # The temporary directory and its contents will be removed automatically when exiting the 'with' block

    return send_file(pdfa_bytes, download_name='output.pdf',
                     as_attachment=True, mimetype='application/pdf')
