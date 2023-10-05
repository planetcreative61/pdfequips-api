import os
from tempfile import NamedTemporaryFile
from flask import after_this_request, jsonify, request, send_file
from tools.split_pdf import split_by_range
from utils.utils import validate_file
"""
    the ranges is a json object and this is how i'm reciving it and passing it to the split_by_range function
"""

import json


def split_pdf_route(app):
    @app.route('/api/split-pdf', methods=['POST'])
    def split_pdf_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        ranges = json.loads(request.form.get('ranges'))  # Convert ranges to JSON object
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            file = files[0]
            split_file = split_by_range(file, ranges)
            with NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
                tmp_file.write(bytes('\n'.join(split_file), 'utf-8'))
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            response = send_file(tmp_file.name, mimetype='application/pdf',
                                 as_attachment=True, download_name='split.pdf', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(tmp_file.name)
                return response

            return response
