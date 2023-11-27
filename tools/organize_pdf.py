"""
    please give me the implementation of this python funciton, it takes two arguments file and pageOrders
    file is a flask pdf file object that needs to be stored before processing as a tmp file.
    pageOrders is an array of numbers that represents the desired page orders.
    for example if a pdf file is uploaded and has 3 pages, and pageOrders is set to [2, 3, 1] then the pdf pages should be re-arranged in the same order, i.e the pages should be 2, 3 and then 1 okay?
    the function should return the path of the generated file. just the string path to the updated file.
"""



import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter

def organize_pdf(file, pageOrders):
   # Save the Flask file object to a temporary file
   temp_file = tempfile.NamedTemporaryFile(delete=False)
   temp_file.write(file.read())
   temp_file.close()

   # Open the PDF file
   input_pdf = PdfReader(temp_file.name)

   # Create a new PDF file
   output_pdf = PdfWriter()

   # Add pages to the new PDF in the desired order
   for page_num in pageOrders:
       output_pdf.add_page(input_pdf.pages[page_num - 1]) # -1 because page numbers start from 0

   # Save the new PDF to a temporary file
   temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
   with open(temp_output_file.name, "wb") as output_stream:
       output_pdf.write(output_stream)

   # Delete the original temporary file
   os.unlink(temp_file.name)

   # Return the path of the new PDF
   return temp_output_file.name
