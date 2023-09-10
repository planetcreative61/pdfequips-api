import os
from tempfile import NamedTemporaryFile
from flask import after_this_request, jsonify, request, send_file
from tools.lock_pdf import lock_multiple_pdf_files, lock_pdf_file

from utils.utils import validate_file


def lock_pdf_route(app):
    @app.route('/api/lock-pdf', methods=['POST'])
    def lock_pdf():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        files = request.files.getlist("files")
        password = request.form.get('password')
        if len(files) == 1:
            file = files[0]
            locked_file = lock_pdf_file(file, password)
            with NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
                tmp_file.write(locked_file)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            response = send_file(tmp_file.name, mimetype='application/pdf',
                                 as_attachment=True, download_name='locked.pdf', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(tmp_file.name)
                return response

            return response
        else:
            return lock_multiple_pdf_files(files, password)
            # response = send_file(zip_file.name, mimetype='application/zip',
            #                      as_attachment=True, download_name='locked.zip', conditional=True)
            # response.headers['X-Accel-Buffering'] = 'no'
            # response.headers['Cache-Control'] = 'no-cache'
            # response.headers['Connection'] = 'close'

            # @after_this_request
            # def remove_file(response):
            #     os.remove(zip_file.name)
            #     return response

            # return response
