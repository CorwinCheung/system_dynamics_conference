import os
import pandas as pd
import csv
import pdfplumber
from docx import Document


def pdf_to_csv(file):
    # use pdfplumber or PyPDF2 to read pdf files
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        raw_text = first_page.extract_text()

    # process the raw_text as needed, then save it into a csv file
    # here I'm just writing the raw text to a csv file
    with open(f"{file}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([raw_text])


def docx_to_csv(file):
    # use python-docx to read docx files
    doc = Document(file)
    raw_text = " ".join([p.text for p in doc.paragraphs])

    # process the raw_text as needed, then save it into a csv file
    # here I'm just writing the raw text to a csv file
    with open(f"{file}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([raw_text])


def xlsx_to_csv(file):
    # use pandas to read xlsx files
    data_xls = pd.read_excel(file, index_col=None)
    data_xls.to_csv(f"{file}.csv", encoding='utf-8')


# mapping from extension to conversion function
CONVERSIONS = {"pdf": pdf_to_csv, "docx": docx_to_csv, "xlsx": xlsx_to_csv}


def convert_files(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(filename):
            base, ext = os.path.splitext(filename)
            ext = ext.lstrip(".")  # remove the leading '.'
            if ext in CONVERSIONS:
                conversion_func = CONVERSIONS[ext]
                conversion_func(filename)
