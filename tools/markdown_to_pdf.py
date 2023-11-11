import tempfile
import subprocess
import os
import shutil
import zipfile
import requests
import json

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
  i got these errors from the below function: Traceback (most recent call last):
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
  File "/workspace/pdfequips-api/tools/markdown_to_pdf.py", line 97, in github_md_files_to_pdf
    f.write(content.decode('utf-8'))
TypeError: write() argument must be str, not bytes
"""

"""
 and the output of the print(response.content) looks like this: 
 b"# Contributor Covenant Code of Conduct\n\n## Our Pledge\n\nWe as members, contributors, and leaders pledge to make participation in our\ncommunity a harassment-free experience for everyone, regardless of age, body\nsize, visible or invisible disability, ethnicity, sex characteristics, gender\nidentity and expression, level of experience, education, socio-economic status,\nnationality, personal appearance, race, caste, color, religion, or sexual\nidentity and orientation.\n\nWe pledge to act and interact in ways that contribute to an open, welcoming,\ndiverse, inclusive, and healthy community.\n\n## Our Standards\n\nExamples of behavior that contributes to a positive environment for our\ncommunity include:\n\n- Demonstrating empathy and kindness toward other people\n- Being respectful of differing opinions, viewpoints, and experiences\n- Giving and gracefully accepting constructive feedback\n- Accepting responsibility and apologizing to those affected by our mistakes,\n  and learning from the experience\n- Focusing on what is best not just for us as individuals, but for the overall\n  community\n\nExamples of unacceptable behavior include:\n\n- The use of sexualized language or imagery, and sexual attention or advances of\n  any kind\n- Trolling, insulting or derogatory comments, and personal or political attacks\n- Public or private harassment\n- Publishing others' private information, such as a physical or email address,\n  without their explicit permission\n- Other conduct which could reasonably be considered inappropriate in a\n  professional setting\n\n## Enforcement Responsibilities\n\nCommunity leaders are responsible for clarifying and enforcing our standards of\nacceptable behavior and will take appropriate and fair corrective action in\nresponse to any behavior that they deem inappropriate, threatening, offensive,\nor harmful.\n\nCommunity leaders have the right and responsibility to remove, edit, or reject\ncomments, commits, code, wiki edits, issues, and other contributions that are\nnot aligned to this Code of Conduct, and will communicate reasons for moderation\ndecisions when appropriate.\n\n## Scope\n\nThis Code of Conduct applies within all community spaces, and also applies when\nan individual is officially representing the community in public spaces.\nExamples of representing our community include using an official e-mail address,\nposting via an official social media account, or acting as an appointed\nrepresentative at an online or offline event.\n\n## Enforcement\n\nInstances of abusive, harassing, or otherwise unacceptable behavior may be\nreported to the community leaders responsible for enforcement at\nmdo@getbootstrap.com.\nAll complaints will be reviewed and investigated promptly and fairly.\n\nAll community leaders are obligated to respect the privacy and security of the\nreporter of any incident.\n\n## Enforcement Guidelines\n\nCommunity leaders will follow these Community Impact Guidelines in determining\nthe consequences for any action they deem in violation of this Code of Conduct:\n\n### 1. Correction\n\n**Community Impact**: Use of inappropriate language or other behavior deemed\nunprofessional or unwelcome in the community.\n\n**Consequence**: A private, written warning from community leaders, providing\nclarity around the nature of the violation and an explanation of why the\nbehavior was inappropriate. A public apology may be requested.\n\n### 2. Warning\n\n**Community Impact**: A violation through a single incident or series of\nactions.\n\n**Consequence**: A warning with consequences for continued behavior. No\ninteraction with the people involved, including unsolicited interaction with\nthose enforcing the Code of Conduct, for a specified period of time. This\nincludes avoiding interactions in community spaces as well as external channels\nlike social media. Violating these terms may lead to a temporary or permanent\nban.\n\n### 3. Temporary Ban\n\n**Community Impact**: A serious violation of community standards, including\nsustained inappropriate behavior.\n\n**Consequence**: A temporary ban from any sort of interaction or public\ncommunication with the community for a specified period of time. No public or\nprivate interaction with the people involved, including unsolicited interaction\nwith those enforcing the Code of Conduct, is allowed during this period.\nViolating these terms may lead to a permanent ban.\n\n### 4. Permanent Ban\n\n**Community Impact**: Demonstrating a pattern of violation of community\nstandards, including sustained inappropriate behavior, harassment of an\nindividual, or aggression toward or disparagement of classes of individuals.\n\n**Consequence**: A permanent ban from any sort of public interaction within the\ncommunity.\n\n## Attribution\n\nThis Code of Conduct is adapted from the [Contributor Covenant][homepage],\nversion 2.1, available at\n[https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].\n\nCommunity Impact Guidelines were inspired by\n[Mozilla's code of conduct enforcement ladder][Mozilla CoC].\n\nFor answers to common questions about this code of conduct, see the FAQ at\n[https://www.contributor-covenant.org/faq][FAQ]. Translations are available at\n[https://www.contributor-covenant.org/translations][translations].\n\n[homepage]: https://www.contributor-covenant.org\n[v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html\n[Mozilla CoC]: https://github.com/mozilla/diversity\n[FAQ]: https://www.contributor-covenant.org/faq\n[translations]: https://www.contributor-covenant.org/translations\n"
"""

def github_md_files_to_pdf(github_md_files):
    if len(github_md_files) == 1:
        file = github_md_files[0]
        url = file['url']
        print(url)
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            tmp_folder = tempfile.mkdtemp()
            tmp_file = os.path.join(tmp_folder, file['name'])
            print(response.content)
            content = response.content
            with open(tmp_file, 'w') as f:
                f.write(content.decode('utf-8'))
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
                    content = response.content
                    with open(tmp_file, 'w') as f:
                        f.write(content.decode('utf-8'))
                    filename_without_ext = os.path.splitext(file['name'])[0]
                    output_file = os.path.join(tmp_folder, f'{filename_without_ext}.pdf')
                    subprocess.run(['mdpdf', tmp_file, '-o', output_file])
                    zipf.write(output_file, f'{filename_without_ext}.pdf')
        return output_zip, tmp_folder
