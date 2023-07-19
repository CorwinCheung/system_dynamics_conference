import os
import pandas as pd
import csv
import pdfplumber
from docx import Document
import numpy as np


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


def year_2020():
    pass


def year_2021():
    dfs_2021 = []
    document_2021 = Document("data/2021 b ISDC.docx")
    for table in document_2021.tables:
        text = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(text)
        dfs_2021.append(df)

    print(len(dfs_2021))
    print("data_type: " + str(type(dfs_2021)))
    print("data_type item: " + str(type(dfs_2021[0])))
    print(dfs_2021[0:7])


def explode_for_multiselect(df, column, specified_options):
    # Create a copy of the DataFrame
    df_copy = df.copy()

    # Split the column's values
    df_copy[column] = df_copy[column].str.split(', ')

    # Explode the DataFrame on the column
    df_copy = df_copy.explode(column)

    # Filter rows based on column's membership in the 'specified_options' list
    df_copy = df_copy[df_copy[column].isin(specified_options)]

    # Get value counts as a dictionary
    value_counts_dict = df_copy[column].value_counts().to_dict()

    return value_counts_dict


def year_2022():
    file_path = "data/2022 conference survey.xlsx"
    df_2022 = pd.read_excel(file_path)
    df_2022 = df_2022.drop("Timestamp", axis=1)
    pd.set_option('display.max_columns', None)
    subset_indices = [0, 1, 25, 26, 27, 28, 29, 35, 36,
                      37, 38, 39, 40]  # Assuming zero-based indexing
    categorical_df_2022 = df_2022.iloc[:, subset_indices]
    print(categorical_df_2022.columns)

    print(
        categorical_df_2022["What is your geographic region?"].value_counts())

    value_counts_dict_1 = categorical_df_2022["How did you attend ISDC 2022?"].value_counts(
    ).to_dict()

    options_for_website_use = [
        'Attend zoom sessions (parallels, WIPs, roundtables, etc)',
        'Attend workshops',
        'Access session chat',
        'View posters or attend poster session',
        'Access session recordings'
    ]

    value_counts_dict_2 = explode_for_multiselect(
        categorical_df_2022, "What did you use the conference WEBSITE for? Please select all that apply.", options_for_website_use)

    value_counts_dict_3 = categorical_df_2022["How many years of experience do you have with system dynamics?"].value_counts(
    ).to_dict()

    value_counts_dict_4 = categorical_df_2022["Have you attended the SD conference before?"].value_counts(
    ).to_dict()

    value_counts_dict_5 = categorical_df_2022["If you attended a conference before, which formats did you experience?"].value_counts(
    ).to_dict()

    value_counts_dict_6 = categorical_df_2022["How do you evaluate this year’s hybrid format as compared to the purely in presence and virtual formats?"].value_counts(
    ).to_dict()

    options_for_future_conferences = [
        'access to recorded sessions',
        'networking in Zoom',
        'availability of pre-recorded talks'
    ]
    value_counts_dict_7 = explode_for_multiselect(
        categorical_df_2022, "Which of the following features, if any, would be worthwhile to continue for future conferences? Please select all that apply.", options_for_future_conferences)

    options_for_profession = [
        'Consulting',
        'Higher education',
        'In-house SD practitioner (private sector)',
        'In-house SD practitioner (public sector)',
        'K-12 education',
        'Research using SD',
        'SD client/customer',
        'Student',
        'Retired',
    ]

    value_counts_dict_8 = explode_for_multiselect(
        categorical_df_2022, "What is your profession? Please select all that apply.", options_for_profession)

    options_for_interest = [
        'Business policy',
        'Teaching',
        'Strategy',
        'Health',
        'Economic dynamics',
        'Energy and resources',
        'Environment and ecology',
        'Information science',
        'Methodology',
        'Operations management and supply chains',
        'Participatory problem solving',
        'Public policy',
        'Security',
        'Social and organizational dynamics',
    ]

    value_counts_dict_9 = explode_for_multiselect(
        categorical_df_2022, "What are your fields of interest? Please select all that apply.", options_for_interest)

    value_counts_dict_10 = categorical_df_2022["What is your geographic region?"].value_counts(
    ).to_dict()

    value_counts_dict_11 = categorical_df_2022["How do you self-identify in terms of gender?"].value_counts(
    ).to_dict()

    value_counts_dict_12 = categorical_df_2022["How old are you?"].value_counts(
    ).to_dict()

    options_for_values = [
        'Location',
        'Topic: System Dynamics',
        'Live presentations',
        'Recordings',
        'Social Interaction',
        'Q & A',
    ]

    value_counts_dict_13 = explode_for_multiselect(
        categorical_df_2022, "Which aspects do you value most when choosing to attend a conference? Select up to 3.", options_for_values)

    # create new DataFrame
    count_categorical_df_2022 = pd.DataFrame(index=["2022"])

    # store the dictionaries as single values in the DataFrame
    value_counts_dicts = {
        "How did you attend ISDC 2022?": value_counts_dict_1,
        "What did you use the conference WEBSITE for? Please select all that apply.": value_counts_dict_2,
        "How many years of experience do you have with system dynamics?": value_counts_dict_3,
        "Have you attended the SD conference before?": value_counts_dict_4,
        "If you attended a conference before, which formats did you experience?": value_counts_dict_5,
        "How do you evaluate this year’s hybrid format as compared to the purely in presence and virtual formats?": value_counts_dict_6,
        "Which of the following features, if any, would be worthwhile to continue for future conferences? Please select all that apply.": value_counts_dict_7,
        "What is your profession? Please select all that apply.": value_counts_dict_8,
        "What are your fields of interest? Please select all that apply.": value_counts_dict_9,
        "What is your geographic region?": value_counts_dict_10,
        "How do you self-identify in terms of gender?": value_counts_dict_11,
        "How old are you?": value_counts_dict_12,
        "Which aspects do you value most when choosing to attend a conference? Select up to 3.": value_counts_dict_13
    }

    for column_name, value_counts_dict in value_counts_dicts.items():
        count_categorical_df_2022.loc["2022",
                                      column_name] = [value_counts_dict]

    print(count_categorical_df_2022)
    print(count_categorical_df_2022.shape)

    count_categorical_df_2022.to_csv("categorical_questions.csv")


def main():
    year_2022()
    # year_2021()

    # Make big csv from pandas dataframe with year, categorical variables, Q1, Q2, Q19-23, Q26-31
    # Make big csv from pandas dataframe with year, boolean variables, Q24-25, Q32-33
    # Make big csv from pandas dataframe with year, numerical ratings, Q3-18
    # Make big csv from pandas dataframe with year, additional response strings, Addition Qs 1-5


if __name__ == "__main__":
    main()
