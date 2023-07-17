import os
import pandas as pd
import csv
import pdfplumber
from docx import Document


cur_path = os.path.dirname(__file__)
true_path = "/Users/corwincheung/Programming/Systems Dynamics Analysis/data"


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


def xlsx_to_csv(file):
    # use pandas to read xlsx files
    data_xls = pd.read_excel(file, index_col=None)
    data_xls.to_csv(f"{file}.csv", encoding='utf-8')


# mapping from extension to conversion function
CONVERSIONS = {"pdf": pdf_to_csv, "xlsx": xlsx_to_csv}


def main():
    file_path = "data/2022 conference survey.xlsx"
    # df_2022 = pd.read_excel(file_path)
    # print(df_2022.head())
    # print(df_2022.shape)
    # print("Columns: ")
    # print(df_2022.columns)
    # print("data_types: " + str(df_2022.dtypes))
    # print(df_2022.dtypes())

    dfs_2021 = []
    document_2021 = Document("data/2021 b ISDC.docx")
    for table in document_2021.tables:
        text = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(text)
        dfs_2021.append(df)

    document_2021 = Document("data/2021 b ISDC.docx")
    df_2021 = document_2021.tables[0]
    data = [[cell.text for cell in row.cells] for row in df_2021.rows]
    df = pd.DataFrame(data)

    print(len(dfs_2021))
    print("data_type: " + str(type(dfs_2021)))
    print("data_type item: " + str(type(dfs_2021[0])))
    print(dfs_2021)

    # Make big csv from pandas dataframe with year, categorical variables, Q1, Q2, Q19-23, Q26-31
    # Make big csv from pandas dataframe with year, boolean variables, Q24-25, Q32-33
    # Make big csv from pandas dataframe with year, numerical ratings, Q3-18
    # Make big csv from pandas dataframe with year, additional response strings, Addition Qs 1-5


if __name__ == "__main__":
    main()
# def convert_files(directory):
#     for filename in os.listdir(directory):
#         if os.path.isfile(filename):
#             base, ext = os.path.splitext(filename)
#             ext = ext.lstrip(".")  # remove the leading '.'
#             if ext in CONVERSIONS:
#                 conversion_func = CONVERSIONS[ext]
#                 conversion_func(filename)
