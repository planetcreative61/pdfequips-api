import os
from tempfile import NamedTemporaryFile
from flask import after_this_request, jsonify, request, send_file
from tools.unlock_pdf import unlock_multiple_pdf_files, unlock_pdf_file


from utils.utils import validate_file


def unlock_pdf_route(app):
    @app.route('/api/unlock-pdf', methods=['POST'])
    def unlock_pdf():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        files = request.files.getlist("files")
        passwords = request.form.getlist('passwords')
        if len(files) == 1:
            file = files[0]
            # Replace with your unlocking logic
            unlocked_file = unlock_pdf_file(file, passwords[0])
            with NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
                tmp_file.write(unlocked_file)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            response = send_file(tmp_file.name, mimetype='application/pdf',
                                 as_attachment=True, download_name='unlocked.pdf', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(tmp_file.name)
                return response

            return response
        else:
            # Replace with your unlocking logic for multiple files
            zip_file_path = unlock_multiple_pdf_files(files, passwords)
            response = send_file(zip_file_path, mimetype='application/zip',
                                 as_attachment=True, download_name='unlocked_files.zip')

            @after_this_request
            def remove_file(response):
                os.remove(zip_file_path)
                return response

            return response
