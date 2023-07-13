import subprocess
from flask import jsonify, send_file
import io
import tempfile
import os

"""
    my production flask app is running on a linux ubuntu enviroment
    and i'm getting these errors from this function:
    [INFO] 127.0.0.1 - - [30/May/2023 14:35:09] "POST /pdf-to-pdf-a HTTP/1.1" 500 -
    Traceback (most recent call last):
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 2551, in __call__
        return self.wsgi_app(environ, start_response)
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 2531, in wsgi_app
        response = self.handle_exception(e)
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 165, in wrapped_function
        return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 2528, in wsgi_app
        response = self.full_dispatch_request()
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 1825, in full_dispatch_request
        rv = self.handle_user_exception(e)
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 165, in wrapped_function
        return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 1823, in full_dispatch_request
        rv = self.dispatch_request()
    File "/home/sanusi/.local/lib/python3.10/site-packages/flask/app.py", line 1799, in dispatch_request
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
    File "/home/sanusi/api/routes/pdf2pdf_A.py", line 18, in pdf_to_pdfa_handler
        return pdf_to_pdfa(pdf_files[0])
    File "/home/sanusi/api/pdf2pdfA_converter.py", line 31, in pdf_to_pdfa
        subprocess.run(gs_command, check=True)
    File "/usr/lib/python3.10/subprocess.py", line 501, in run
        with Popen(*popenargs, **kwargs) as process:
    File "/usr/lib/python3.10/subprocess.py", line 969, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
    File "/usr/lib/python3.10/subprocess.py", line 1845, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: 'gswin64'
"""

def pdf_to_pdfa(input_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file_path = os.path.join(temp_dir, 'input.pdf')
        output_file_path = os.path.join(temp_dir, 'output.pdf')

        # Save the FileStorage object to a temporary file
        with open(input_file_path, 'wb') as temp_input_file:
            temp_input_file.write(input_file.read())

        try:
            gs_command = [
                'gs',
                '-dPDFA',
                '-dBATCH',
                '-dNOPAUSE',
                '-dUseCIEColor',
                '-sProcessColorModel=DeviceCMYK',
                '-sDEVICE=pdfwrite',
                '-sPDFACompatibilityPolicy=1',
                f'-sOutputFile={output_file_path}',
                input_file_path
            ]
            subprocess.run(gs_command, check=True)

        except subprocess.CalledProcessError:
            return jsonify({"error": "Conversion to PDF/A failed"}), 400

        with open(output_file_path, 'rb') as pdfa_file:
            pdfa_bytes = io.BytesIO(pdfa_file.read())

        pdfa_bytes.seek(0)

        # The temporary directory and its contents will be removed automatically when exiting the 'with' block

    return send_file(pdfa_bytes, download_name='output.pdf',
                     as_attachment=True, mimetype='application/pdf')
