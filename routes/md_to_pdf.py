import os
import shutil
from flask import jsonify, request, send_file, after_this_request
from tools.markdown_to_pdf import markdown_to_pdf, markdown_to_pdf_multiple
from utils.utils import validate_file
import json

def markdown_to_pdf_route(app):
    @app.route('/api/markdown-to-pdf', methods=['POST'])
    def markdown_to_pdf_file():
        print("accessed")
        if 'files' not in request.files:
            return jsonify({"error": "No markdown file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            converted_file = markdown_to_pdf(files[0])
            response = send_file(converted_file, mimetype='application/pdf',
                                 as_attachment=True, download_name='converted.pdf', conditional=True)

            @after_this_request
            def remove_file(response):
                os.remove(converted_file)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        # else:
        #     zip_file, temp_directory = markdown_to_pdf_multiple(files=files)
        #     response = send_file(zip_file, mimetype='application/zip',
        #                          as_attachment=True, download_name='output.zip', conditional=True)
        #     response.headers['X-Accel-Buffering'] = 'no'
        #     response.headers['Cache-Control'] = 'no-cache'
        #     response.headers['Connection'] = 'close'

        #     @after_this_request
        #     def remove_file(response):
        #         os.remove(zip_file)
        #         shutil.rmtree(temp_directory)
        #         return response

        #     return response
