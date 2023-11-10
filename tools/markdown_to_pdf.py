import tempfile
import subprocess
import os
import shutil
import zipfile

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
                output_file = os.path.join(tmp_folder, f'{file.filename}.pdf')
                subprocess.run(['mdpdf', tmp_file, '-o', output_file])
                zipf.write(output_file, f'{file.filename}.pdf')
        return output_zip, tmp_folder
