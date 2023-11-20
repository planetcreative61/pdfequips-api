import os
import zipfile
import tempfile
import subprocess


def pdf_to_html(file):
 print(file)
 try:
     with tempfile.TemporaryDirectory() as temp_dir:
         temp_pdf_path = os.path.join(temp_dir, 'temp.pdf')
         file.save(temp_pdf_path)

         temp_html_path = os.path.join(temp_dir, 'temp.html')

         command = f'pdftohtml -c -noframes -stdout "{temp_pdf_path}" > "{temp_html_path}"'
         subprocess.run(command, shell=True)

         if os.path.exists(temp_html_path):
             return temp_html_path
         else:
             html_files = [f for f in os.listdir(temp_dir) if f.endswith('.html')]
             with zipfile.ZipFile(os.path.join(temp_dir, 'html_files.zip'), 'w') as zipf:
                for html_file in html_files:
                    zipf.write(os.path.join(temp_dir, html_file), html_file)
             return os.path.join(temp_dir, 'html_files.zip')
 except Exception as e:
     print(f"Error: {e}")
     return None


def pdf_to_html_multiple():
    pass