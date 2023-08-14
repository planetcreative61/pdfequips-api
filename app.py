# Making sure we have the necessary imports:
# pip install opencv-python-headless
# from flask_cors import CORS
from flask import Flask


from jinja2 import FileSystemLoader
from werkzeug.middleware.proxy_fix import ProxyFix

from routes.compresspdf_route import compress_pdf_route
from routes.excel2pdf import excel_to_pdf_route
from routes.html2pdf import html_to_pdf_route
# from . import img2pdf

from routes.img_2pdf import jpg_to_pdf_route
from routes.mergepdfs import merge_pdfs_route
from routes.pdf2excel import pdf_to_excel_route
from routes.pdf2img import pdf_to_jpg_route
from routes.pdf2pdf_A import pdf_to_pdfa_route
from routes.pdf2ppt import pdf_to_ppt_route
from routes.pdf2word import pdf_to_word_route
from routes.ppt2pdf import ppt_to_pdf_route
from routes.word2pdf import word_to_pdf_route
from routes.pdf2text import pdf_to_text_route
# from .utils import is_pdf, upload_file

# from compress_pdf import compress_pdf
# from werkzeug.utils import secure_filename

# from flask import abort
from PIL import Image

# only for DEVELOPMENT
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


app = Flask(__name__)

# cors
# CORS(app)


# setting templates directory for get routes
# app.wsgi_app = ProxyFix(app.wsgi_app)
# app.jinja_loader = FileSystemLoader('/out')
# setting uploads folder


# converter routes
jpg_to_pdf_route(app)
pdf_to_jpg_route(app)
word_to_pdf_route(app)
pdf_to_word_route(app)
ppt_to_pdf_route(app)
html_to_pdf_route(app)
pdf_to_pdfa_route(app)
excel_to_pdf_route(app)
pdf_to_excel_route(app)
pdf_to_ppt_route(app)
compress_pdf_route(app)
pdf_to_text_route(app)
# other pdf tool routes
merge_pdfs_route(app)
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)

