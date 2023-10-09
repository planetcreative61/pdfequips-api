# i want another function similar to this but for extract-pages route
import os
from flask import jsonify, request, send_file
from tools.split_by_range import split_by_range
from utils.utils import validate_file
import json

def split_by_range_route(app):
    @app.route('/api/split-by-range', methods=['POST'])
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
            file = files[0]
            split_file_path, output_files = split_by_range(file, ranges)
            if not split_file_path:
                return jsonify({"error": "Error splitting PDF"}), 500
            try:
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

            finally:
                os.remove(split_file_path)
                for file_path in output_files:
                    os.remove(file_path)
            return response
        else:
            try:
                zip_file_path, output_files = split_by_range(files, ranges)
                if not zip_file_path:
                    return jsonify({"error": "Error splitting PDF"}), 500
                response = send_file(zip_file_path, mimetype='application/zip',
                                     as_attachment=True, download_name='split.zip', conditional=True)
                response.headers['X-Accel-Buffering'] = 'no'
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Connection'] = 'close'
            finally:
                os.remove(zip_file_path)
                for file_path in output_files:
                    os.remove(file_path)
            return response
