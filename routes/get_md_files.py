from flask import Flask, request, jsonify
import requests
import os


"""
    please change the implementation of this function where it also includes the url of the file in the response
    i.e add a url entity to the markdown_files which is the url of the current md file
"""
def get_md_files(app):
    @app.route('/api/get-md-files', methods=['GET'])
    def get_md_files_handler():
        url = request.args.get('url')
        url_parts = url.split("/")
        owner = url_parts[3]
        repo = url_parts[4]
        path = "/".join(url_parts[7:])  # Skip the '/tree/main/' part

        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {os.getenv('GITHUB_API_KEY')}",
            },
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):  # Check if data is an array, indicating a directory
                markdown_files = [
                    {
                        "name": file['name'],
                        "size": file['size'],
                        "url": file['html_url']
                    }
                    for file in data if file['type'] == 'file' and file['name'].endswith('.md')
                ]
            else:  # If data is not an array, it's a single file
                if data['type'] == 'file' and data['name'].endswith('.md'):
                    markdown_files = [
                        {
                            "name": data['name'],
                            "size": data['size'],
                            "url": data['html_url']
                        }
                    ]
                else:
                    markdown_files = []
            return jsonify(markdown_files), 200
        else:
            return jsonify({"error": "Failed to fetch repository contents"}), 400
