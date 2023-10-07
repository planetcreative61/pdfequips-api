# sudo apt-get install poppler-utils
# here is the updated code, it's still not working as expected
# gitpod /workspace/pdfequips-api (master) $ ls /tmp
# files-0.pdf  files-1.pdf  files-2.pdf
"""
   i want a function called split_by_range 
"""

# this is how i'm using the function:

import os
from tempfile import NamedTemporaryFile
from flask import after_this_request, jsonify, request, send_file
from tools.split_pdf import split_by_range
from utils.utils import validate_file
import json

def split_pdf_route(app):
    @app.route('/api/split-pdf', methods=['POST'])
    def split_pdf_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        # Convert ranges to JSON object
        ranges = json.loads(request.form.get('ranges'))
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            # file = files[0]
            file = files[0]
            split_file_path = split_by_range(file, ranges)
            if not split_file_path:
                return jsonify({"error": "Error splitting PDF"}), 500
            if split_file_path.endswith('.pdf'):
                mimetype = 'application/pdf'
                download_name = 'split.pdf'
            else:  # It's a zip file
                mimetype = 'application/zip'
                download_name = 'split.zip'
            response = send_file(split_file_path, mimetype=mimetype,
                                 as_attachment=True, download_name=download_name, conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(split_file_path)
                return response

            return response
        else:
            zip_file_path = split_by_range(files, ranges)
            if not zip_file_path:
                return jsonify({"error": "Error splitting PDF"}), 500
            response = send_file(zip_file_path, mimetype='application/zip',
                                 as_attachment=True, download_name='split.zip', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(zip_file_path)
                return response

            return response

