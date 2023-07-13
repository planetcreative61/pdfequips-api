import os
import tempfile
import subprocess
import zipfile
from flask import send_file

"""
    a python function called pdf_to_jpg_converter which takes a pdf file using ghostscript, i have it installed as gs,
    i'll be using the function on my flask app like this: return pdf_to_jpg_converter(request.files.getlist('files'))
    this function should loop through all the pdf file pages and generate an image for each page,
    Every page of this PDF will be converted into a JPG file.
    each image file name should be the same name as the pdf file name + a number
    for example:
    uploaded file: resume.pdf and it contains 2 pages.
    converted files: resume-01.jpg, resume-02.jpg
    and the returned value should be a zip file containing all converted images if the original pdf file consist of many pages,
    one jpg file if the oriringinal pdf file contains only one page, and the jpg file name should be the same as the pdf file but with .jpg extension.
    finally at last the original pdf file should be removed from the tmp folder as well as the converted jpg files.
    return value of the function should be zip folder or .jpg file.
"""



def pdf_to_jpg_converter(pdf_files):
    output_dir = tempfile.mkdtemp()
    jpg_files = []
    for pdf_file in pdf_files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            pdf_file.seek(0)
            temp.write(pdf_file.read())
            temp_path = temp.name

        subprocess.run(["gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=jpeg", "-r150", f"-sOutputFile={output_dir}/%d.jpg", temp_path])

        pdf_filename = os.path.splitext(os.path.basename(pdf_file.filename))[0]
        page_count = len(os.listdir(output_dir))
        for i in range(1, page_count+1):
            jpg_filename = f"{pdf_filename}-{i:02d}.jpg"
            jpg_path = os.path.join(output_dir, f"{i}.jpg")
            os.rename(jpg_path, os.path.join(output_dir, jpg_filename))
            jpg_files.append(os.path.join(output_dir, jpg_filename))

        os.remove(temp_path)

    if len(jpg_files) == 1:
        response = send_file(jpg_files[0], as_attachment=True, mimetype='image/jpeg')
        os.remove(jpg_files[0])
    else:
        with zipfile.ZipFile(os.path.join(output_dir, "converted_files.zip"), mode="w") as archive:
            for jpg_file in jpg_files:
                archive.write(jpg_file, os.path.basename(jpg_file))
                os.remove(jpg_file)
        response = send_file(os.path.join(output_dir, "converted_files.zip"), as_attachment=True, mimetype='application/zip')
        os.remove(os.path.join(output_dir, "converted_files.zip"))

    os.rmdir(output_dir)

    return response




def pdf_to_jpg_converter_multiple(pdf_files):
    output_dir = tempfile.mkdtemp()
    zip_filename = "converted_files.zip"
    zip_filepath = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_filepath, mode="w") as archive:
        for pdf_file in pdf_files:
            pdf_filename = os.path.splitext(os.path.basename(pdf_file.filename))[0]
            pdf_dir = os.path.join(output_dir, pdf_filename)
            os.mkdir(pdf_dir)
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
                pdf_file.seek(0)
                temp.write(pdf_file.read())
                temp_path = temp.name

            subprocess.run(["gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=jpeg", "-r150", f"-sOutputFile={pdf_dir}/%d.jpg", temp_path])
            os.remove(temp_path)

            page_count = len(os.listdir(pdf_dir))
            jpg_files = []
            for i in range(1, page_count+1):
                jpg_filename = f"{pdf_filename}-{i:02d}.jpg"
                jpg_path = os.path.join(pdf_dir, f"{i}.jpg")
                os.rename(jpg_path, os.path.join(pdf_dir, jpg_filename))
                jpg_files.append(os.path.join(pdf_dir, jpg_filename))

            for jpg_file in jpg_files:
                archive.write(jpg_file, os.path.join(pdf_filename, os.path.basename(jpg_file)))
                os.remove(jpg_file)

            os.rmdir(pdf_dir)

    response = send_file(zip_filepath, as_attachment=True, mimetype='application/zip')
    os.remove(zip_filepath)
    os.rmdir(output_dir)

    return response