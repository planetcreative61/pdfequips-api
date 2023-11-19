import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
from tools.ocr_pdf import ocr_pdf
import json

def ocr_pdf_route(app):
    @app.route('/api/ocr-pdf', methods=['POST'])
    def ocr_pdf_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        
        selected_languages = request.form.getlist('selectedLanguages')
        if not selected_languages:
            return jsonify({"error": "No languages provided"}), 400
        
        if len(files) == 1:
            result = ocr_pdf(files[0], selected_languages)
            
            response = send_file(result, mimetype='application/pdf', as_attachment=True, download_name='ocr_result.pdf', conditional=True)
            
            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            
            return response
        
        # For multiple files
        # else:
        #     zip_file, temp_directory = ocr_pdf_multiple(
        #         files=files, selected_languages=selected_languages)
        #
        #     response = send_file(zip_file, mimetype='application/zip', as_attachment=True, download_name='output.zip', conditional=True)
        #
        #     @after_this_request
        #     def remove_file(response):
        #         os.remove(zip_file)
        #         shutil.rmtree(temp_directory)
        #         return response
        #
        #     return response