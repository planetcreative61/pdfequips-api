from flask import request, jsonify, send_file
from pdf2text_converter import pdf_to_text, pdf_to_text_multiple
from utils.utils import validate_file
import os
from tempfile import NamedTemporaryFile

"""
    this function right now, is converting all the pdf files into one txt file if multiple files are uploaded
    instead it should return a zip folder containing each converted txt file in it.
"""

def pdf_to_text_route(app):
    @app.route('/pdf-to-text', methods=['POST'])
    def convert_pdf_to_text():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        files = request.files.getlist("files")
        if len(files) == 1:
            file = files[0]
            text = pdf_to_text(file)
            with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
                tmp_file.write(text)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            return send_file(tmp_file.name, mimetype='text/plain', as_attachment=True, download_name='output.txt')
        else:
            zip_file = pdf_to_text_multiple(files)
            return send_file(zip_file.name, mimetype='application/zip', as_attachment=True, download_name='output.zip')
