import shutil
import os
import sys
import re
from PyPDF2 import PdfReader
from docx import Document
from pathlib import Path


def get_extension(source_path):
    return Path(source_path).suffix

def create_tex_path(source_path):
    filename = os.path.splitext(os.path.basename(source_path))[0]
    tex_filename = filename + ".tex"
    tex_path = os.path.join(os.path.dirname(source_path), tex_filename)
    return tex_path

def process_pdf_nwlines(page_text):
    bibliography = False
    processed_text = ""

    split_lines = page_text.split('\n')
    for i in range(len(split_lines)):
        if "Bibliographie " in split_lines[i]:
            bibliography = True
        
        if bibliography:
            processed_text += split_lines[i] + "\n"
        else:
            line = split_lines[i]
            if i + 1 < len(split_lines):
                next_line = split_lines[i + 1] 
            else: 
                next_line = ""
            if line.endswith(" ") and next_line and (next_line[0].isalnum() or (next_line[0].isspace() and len(next_line))):
                processed_text += line.rstrip() + " "
            else:
                processed_text += line + "\n\n"

    return processed_text

def pdf_to_tex(source_path, tex_path):

    with open(source_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        tex_writer = open(tex_path, 'w')

        with open(tex_path, 'w') as tex_writer:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                processed_text = process_pdf_nwlines(page_text) 
                tex_writer.write(processed_text)

        tex_writer.close()
        
    print(f"PDF copied in .tex: {tex_path}")
    return

def docx_to_tex(source_path, tex_path):
    document = Document(source_path)

    with open(tex_path, 'w', encoding='utf-8') as tex_file:
        for para in document.paragraphs:
            tex_file.write(para.text + "\n")




# if __name__ == "__name__":
print("pdf_to_tex: Author Floriane TUERNAL-SABOTINOV")
print("This program is at early stage. Please, be kind enough to signal any problem or improvements you would like to see in the future.")
print("")
print("")
print("")

if len(sys.argv) != 2:
     print("Usage: python3 pdf_to_tex.py path/to/the/file")
     sys.exit(1)

source_path = sys.argv[1]
if not os.path.exists(source_path):
    print("Path error")
    sys.exit(1)

tex_path = create_tex_path(source_path)
if get_extension(source_path) == ".pdf":
    pdf_to_tex(source_path, tex_path)
elif get_extension(source_path) == ".docx":
    docx_to_tex(source_path, tex_path)
else:
    print("Error: File extension is not supported yet")

