import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from tools.translate_pdf import translate_pdf
from utils.utils import validate_file
import json
def translate_pdf_route(app):
    @app.route('/api/translate-pdf', methods=['POST'])
    def translate_pdf_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        from_language = request.form.get('from_language')
        to_language = request.form.get('to_language')
        if not from_language or not to_language:
            return jsonify({"error": "No translation languages provided"}), 400
        if len(files) == 1:
            translated_file = translate_pdf(files[0], from_language, to_language)
            response = send_file(translated_file, mimetype='application/pdf',
                                 as_attachment=True, download_name='translated.pdf', conditional=True)

            @after_this_request
            def remove_file(response):
                os.remove(translated_file)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        # else:
        #     zip_file, temp_directory = translate_pdf_multiple(
        #         files=files, from_language=from_language, to_language=to_language)
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
