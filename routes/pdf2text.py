from flask import request, jsonify, send_file
from pdf2text_converter import pdf_to_text
from utils.utils import validate_file
# the response type for the text file served should be text it should be a text file.
"""
    this is the definition of the pdf_to_text function
    def pdf_to_text(file):
        pdf_reader = PdfReader(file)
        text = StringIO()
        for page in pdf_reader.pages:
            text.write(page.extract_text())
        return text.getvalue()
"""

import os
from tempfile import NamedTemporaryFile


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
            texts = []
            for file in files:
                text = pdf_to_text(file)
                texts.append(text)
            with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
                tmp_file.write('\n'.join(texts))
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            return send_file(tmp_file.name, mimetype='text/plain', as_attachment=True, download_name='output.txt')
