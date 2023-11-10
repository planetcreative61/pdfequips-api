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
    i have a GITHUB_API_KEY env variable that can be used to access the github api
    please use it to implement this function for me, it's taking a github urls list
    save each file in the list as a tmp file and convert it to pdfs using the same approach as the md_to_pdf function.
    or use it if it's possible.
"""


def github_md_files_to_pdf(github_md_files):
    tmp_folder = tempfile.mkdtemp()
    if len(github_md_files) == 1:
        file_info = github_md_files[0]
        url = file_info['name']
        response = requests.get(url, headers={'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'})
        filename_without_ext = os.path.splitext(os.path.basename(url))[0]
        tmp_file = os.path.join(tmp_folder, f'{filename_without_ext}.md')
        with open(tmp_file, 'w') as f:
            f.write(response.text)
        output_file = os.path.join(tmp_folder, f'{filename_without_ext}.pdf')
        subprocess.run(f'mdpdf {tmp_file} -o {output_file} > /dev/null 2>&1', shell=True)
        return output_file, tmp_file
    else:
        output_zip = os.path.join(tmp_folder, 'output.zip')
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for file_info in github_md_files:
                url = file_info['name']
                response = requests.get(url, headers={'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'})
                filename_without_ext = os.path.splitext(os.path.basename(url))[0]
                tmp_file = os.path.join(tmp_folder, f'{filename_without_ext}.md')
                with open(tmp_file, 'w') as f:
                    f.write(response.text)
                output_file = os.path.join(tmp_folder, f'{filename_without_ext}.pdf')
                subprocess.run(f'mdpdf {tmp_file} -o {output_file} > /dev/null 2>&1', shell=True)
                zipf.write(output_file, f'{filename_without_ext}.pdf')
        return output_zip, tmp_folder
