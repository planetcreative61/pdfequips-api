import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from tools.number_pdf import number_pdf
from utils.utils import validate_file
import json
def number_pdf_route(app):
    @app.route('/api/number-pdf', methods=['POST'])
    def number_pdf_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        options_json = request.form.get('options')
        if not options_json:
            return jsonify({"error": "No options provided"}), 400
        options = json.loads(options_json)
        if len(files) == 1:
            # Call the number_pdf function with the files and options
            # Replace the following line with your actual implementation
            result = number_pdf(files[0], options)
            # Return the result as a response
            # Replace the following line with your actual implementation
            response = send_file(result, mimetype='application/pdf',
                                 as_attachment=True, download_name='numbered.pdf', conditional=True)

            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        # else:
        #     # Call the number_pdf_multiple function with the files and options
        #     # Replace the following line with your actual implementation
        #     zip_file, temp_directory = number_pdf_multiple(
        #         files=files, options=options)
        #     # Return the zip_file as a response
        #     # Replace the following line with your actual implementation
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
