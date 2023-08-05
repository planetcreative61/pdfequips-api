from flask import request, jsonify, send_file, after_this_request
from pdf2text_converter import pdf_to_text, pdf_to_text_multiple
from utils.utils import validate_file
import os
from tempfile import NamedTemporaryFile


def pdf_to_text_route(app):
    @app.route('/api/pdf-to-text', methods=['POST'])
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
            response = send_file(tmp_file.name, mimetype='text/plain',
                                 as_attachment=True, download_name='output.txt', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(tmp_file.name)
                return response

            return response
        else:
            zip_file = pdf_to_text_multiple(files)
            response = send_file(zip_file.name, mimetype='application/zip',
                                 as_attachment=True, download_name='output.zip', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(zip_file.name)
                return response

            return response
