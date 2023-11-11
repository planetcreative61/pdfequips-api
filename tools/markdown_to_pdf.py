import tempfile
import subprocess
import os
import shutil
import zipfile
import requests


def md_text_to_pdf(md_text):
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.md') as temp:
        temp.write(md_text)
        temp_path = temp.name

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.pdf') as temp_pdf:
        pdf_path = temp_pdf.name

    subprocess.run(['mdpdf', temp_path, '-o', pdf_path], check=True)

    return temp_path, pdf_path



def md_to_pdf(files):
    if len(files) == 1:
        file = files[0]
        tmp_folder = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_folder, file.filename)
        file.save(tmp_file)
        output_file = os.path.join(tmp_folder, 'output.pdf')
        subprocess.run(['mdpdf', tmp_file, '-o', output_file])
        return output_file, tmp_file
    else:
        tmp_folder = tempfile.mkdtemp()
        output_zip = os.path.join(tmp_folder, 'output.zip')
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for file in files:
                tmp_file = os.path.join(tmp_folder, file.filename)
                file.save(tmp_file)
                filename_without_ext = os.path.splitext(file.filename)[0]
                output_file = os.path.join(tmp_folder, f'{filename_without_ext}.pdf')
                subprocess.run(['mdpdf', tmp_file, '-o', output_file])
                zipf.write(output_file, f'{filename_without_ext}.pdf')
        return output_zip, tmp_folder


"""
    
    please give me the implementation of this function, it's taking a github urls list
    save each file in the list as a tmp file and convert it to pdfs using the same approach as the md_to_pdf function.
    or use it if it's possible.
    keep in mind that the github_md_files is a dictionary i.e an object that is comming from the front end as json:
    which is in the following format: { name: string; size: number }[];
"""


"""
    in this function before i was using response.content as the file content but it's a json file
    instead i realized that in the content json there is a richText property which contains the md text, i want to use that.
    but i got these errors:
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
  File "/workspace/pdfequips-api/routes/md_to_pdf.py", line 40, in md_to_pdf_handler
    pdf_path, tmp_path = github_md_files_to_pdf(selectedGithubMarkdownUrls)
  File "/workspace/pdfequips-api/tools/markdown_to_pdf.py", line 65, in github_md_files_to_pdf
    f.write(response.content.richText)
AttributeError: 'bytes' object has no attribute 'richText'
"""

def github_md_files_to_pdf(github_md_files):
    if len(github_md_files) == 1:
        file = github_md_files[0]
        url = file['url']
        response = requests.get(url)
        if response.status_code == 200:
            tmp_folder = tempfile.mkdtemp()
            tmp_file = os.path.join(tmp_folder, file['name'])
            content = response.json()['content']['richText']
            with open(tmp_file, 'w') as f:
                f.write(content)
            output_file = os.path.join(tmp_folder, 'output.pdf')
            subprocess.run(['mdpdf', tmp_file, '-o', output_file])
            return output_file, tmp_folder
        else:
            return None, None
    else:
        tmp_folder = tempfile.mkdtemp()
        output_zip = os.path.join(tmp_folder, 'output.zip')
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for file in github_md_files:
                url = file['url']
                response = requests.get(url)
                if response.status_code == 200:
                    tmp_file = os.path.join(tmp_folder, file['name'])
                    content = response.json()['content']['richText']
                    with open(tmp_file, 'w') as f:
                        f.write(content)
                    filename_without_ext = os.path.splitext(file['name'])[0]
                    output_file = os.path.join(tmp_folder, f'{filename_without_ext}.pdf')
                    subprocess.run(['mdpdf', tmp_file, '-o', output_file])
                    zipf.write(output_file, f'{filename_without_ext}.pdf')
        return output_zip, tmp_folder
