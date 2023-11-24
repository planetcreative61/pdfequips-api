import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
from tools.remove_pages import remove_pages
import json

def remove_pages_route(app):
    @app.route('/api/remove-pages', methods=['POST'])
    def remove_pdf_files():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        
        selectedPages = request.form.get('selectedPages')
        
        if len(files) == 1:
            result = remove_pages(files[0], selectedPages)
            
            response = send_file(result, mimetype='application/pdf', as_attachment=True, download_name='ocr_result.pdf', conditional=True)
            
            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            
            return response