import os
from flask import send_from_directory

app_dir = os.path.dirname(os.path.abspath(__file__))

def get_routes_handler(app):
    STATIC_FILES = ['logo.png', 'pdf.worker.js']

    @app.route('/', methods=['GET'])
    def index():
        try:
            return send_from_directory(os.path.join(app_dir, '../../'), 'index.html')
        except:
            return "404 Not Found", 404

    @app.route('/images/<path:image_name>')
    def serve_image(image_name):
        valid_extensions = ['jpg', 'png']
        extension = image_name.split('.')[-1]
        if extension not in valid_extensions:
            return "Invalid file type", 400
        try:
            return send_from_directory(os.path.join(app_dir, '../../images'), image_name)
        except:
            return "404 Not Found", 404
            
    @app.route('/<path:path>', methods=['GET'])
    def serve_static(path):
        if path in STATIC_FILES:
            try:
                return send_from_directory(os.path.join(app_dir, '../../'), path)
            except:
                return "404 Not Found", 404
        else:
            try:
                return send_from_directory(os.path.join(app_dir, '../../'), path + '.html')
            except:
                return "404 Not Found", 404

    @app.route('/_next/<path:path>', methods=['GET'])
    def serve_next_static(path):
        try:
            return send_from_directory(os.path.join(app_dir, '../../_next'), path)
        except:
            return "404 Not Found", 404