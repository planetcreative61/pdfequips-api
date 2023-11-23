import io
import os
import tempfile
import pytesseract

"""
   this ocr_pdf function takes a flask file object that needs to be saved as a tmp file before processing,
   and it also takes a selectedLanguages which is a list of language codes like "en" or "fr" and so on.
   it should increase the accurecy of the OCR.
   please show me how can we solve this problem?
"""



from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os




import tempfile
import subprocess
import os


"""
    the below ocr_pdf function is suppose to convert a scanned pdf file into a selectable and serchable version of the same document and preserving styleing and fonts and layouts and everthing from the oririnal document.
    but i got these errors:
     * Debug mode: on
Tesseract Open Source OCR Engine v4.1.1 with Leptonica
Error in pixReadStream: Pdf reading is not supported
Error in pixRead: pix not read
Error during processing.
Traceback (most recent call last):
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2548, in __call__
    return self.wsgi_app(environ, start_response)
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2528, in wsgi_app
    response = self.handle_exception(e)
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2525, in wsgi_app
    response = self.full_dispatch_request()
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1822, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1820, in full_dispatch_request
    rv = self.dispatch_request()
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1796, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/workspace/pdfequips-api/routes/ocr_pdf.py", line 28, in ocr_pdf_file
    response = send_file(result, mimetype='application/pdf', as_attachment=True, download_name='ocr_result.pdf', conditional=True)
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/helpers.py", line 537, in send_file
    return werkzeug.utils.send_file(  # type: ignore[return-value]
  File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/werkzeug/utils.py", line 440, in send_file
    stat = os.stat(path)
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmpusmymbbv.pdf_ocr.pdf'

"""
import os
import subprocess
import tempfile
from flask import send_file

def ocr_pdf(file, o):
    # create a temporary file to save the uploaded file
    tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    file.save(tmp_file.name)
    
    # convert the PDF to an image using Ghostscript
    img_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    subprocess.run(["gs", "-sDEVICE=png16m", "-r300", "-o", img_file.name, tmp_file.name])
    
    # use tesseract to convert the image into a selectable pdf file
    # you need to have tesseract installed on your system and in your PATH
    # you can also specify other options for tesseract, such as language or output format
    # see the documentation for more details: [1]
    output_file = tmp_file.name + "_ocr"
    subprocess.run(["tesseract", img_file.name, output_file, "-l", "eng", "pdf"])
    
    # delete the temporary files
    os.remove(tmp_file.name)
    os.remove(img_file.name)
    
    # return the output file name
    return output_file
