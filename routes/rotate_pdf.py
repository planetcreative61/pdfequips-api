import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from tools.rotate_pdf import rotate_pdf, rotate_pdf_multiple
from utils.utils import validate_file
import json

"""
    i want another route function like the below but for /api/translate-pdf
    which is the same but accepts a from_language and to_language from the front end and passes it to translate_pdf & translate_pdf_multiple
"""
def rotate_pdf_route(app):
    @app.route('/api/rotate-pdf', methods=['POST'])
    def rotate_pdf_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        angles_json = request.form.get('angles')
        if not angles_json:
            return jsonify({"error": "No rotation angle provided"}), 400
        angles = json.loads(angles_json)
        if len(files) == 1:
            angle_values = [angle['value'] for angle in angles]
            rotated_file = rotate_pdf(files[0], angle_values[0])
            response = send_file(rotated_file, mimetype='application/pdf',
                                 as_attachment=True, download_name='rotated.pdf', conditional=True)

            @after_this_request
            def remove_file(response):
                os.remove(rotated_file)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        else:
            zip_file, temp_directory = rotate_pdf_multiple(
                files=files, angles=angles)
            response = send_file(zip_file, mimetype='application/zip',
                                 as_attachment=True, download_name='output.zip', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(zip_file)
                shutil.rmtree(temp_directory)
                return response

            return response
