import os
from flask import jsonify, request, send_file
from tools.extact_pages import extract_pages
from utils.utils import validate_file


def extract_pages_route(app):
    @app.route('/api/extract-pages', methods=['POST'])
    def extract_pages_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400

        # files =
        files = request.files.getlist('files')
        # Convert ranges to JSON object
        selected_pages = request.form.get('selectedPages')
        merge = request.form.get('merge')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            file = files[0]
            retval = extract_pages(
                file, selected_pages, merge)
            if not retval:
                return jsonify({"error": "Error splitting PDF"}), 500
            try:
                if retval[0].endswith('.pdf'):
                    mimetype = 'application/pdf'
                    download_name = 'split.pdf'
                else:  # It's a zip file
                    split_file_path, output_files = retval
                    mimetype = 'application/zip'
                    download_name = 'split.zip'
                response = send_file(retval[0], mimetype=mimetype,
                                     as_attachment=True, download_name=download_name, conditional=True)
                response.headers['X-Accel-Buffering'] = 'no'
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Connection'] = 'close'

            finally:
                os.remove(split_file_path)
                for file_path in output_files:
                    os.remove(file_path)
            return response
