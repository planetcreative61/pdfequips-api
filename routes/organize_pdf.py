import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
from tools.organize_pdf import organize_pdf
import json

def organize_pdf_route(app):
    @app.route('/api/organize-pdf', methods=['POST'])
    def organize_pdf_files():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        pageOrders = json.loads(request.form.get('pageOrders'))
        
        if len(files) == 1:
            result = organize_pdf(files[0], pageOrders)
            
            response = send_file(result, mimetype='application/pdf', as_attachment=True, download_name='ocr_result.pdf', conditional=True)
            
            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            
            return response