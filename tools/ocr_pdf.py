import os
import subprocess
import tempfile
from flask import send_file

def ocr_pdf(file, o):
    # create a temporary file to save the uploaded file
    tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    file.save(tmp_file.name)
    print(f"Saved uploaded file to {tmp_file.name}")
    
    # convert the PDF to images using Ghostscript
    # each page will be output as a separate image
    img_files = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    subprocess.run(["gs", "-sDEVICE=png16m", "-r300", "-o", img_files.name + "%d", tmp_file.name])
    print(f"Converted PDF to images: {img_files.name}%d")
    
    # use tesseract to convert each image into a selectable pdf file
    # you need to have tesseract installed on your system and in your PATH
    # you can also specify other options for tesseract, such as language or output format
    # see the documentation for more details: [1]
    output_files = []
    for i in range(1, 100):  # assuming the PDF has less than 100 pages
        if os.path.exists(img_files.name + str(i)):
            output_file = tmp_file.name + "_ocr" + str(i)
            subprocess.run(["tesseract", img_files.name + str(i), output_file, "-l", "eng", "pdf"])
            print(f"Processed image with Tesseract: {output_file}.pdf")
            output_files.append(output_file + ".pdf")
        else:
            break
    
    # combine the output files into a single PDF
    final_output_file = tmp_file.name + "_ocr_final.pdf"
    subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite", "-sOutputFile=" + final_output_file] + output_files)
    print(f"Combined output files into: {final_output_file}")
    
    # delete the temporary files
    os.remove(tmp_file.name)
    for i in range(1, len(output_files) + 1):
        os.remove(img_files.name + str(i))
        os.remove(tmp_file.name + "_ocr" + str(i) + ".pdf")
    
    # return the output file name
    return final_output_file
