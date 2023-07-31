import os
import pandas as pd
from docx import Document
import numpy as np
import re

cur_path = os.path.dirname(__file__)
true_path = "/Users/corwincheung/Programming/Systems Dynamics Analysis/data"


def year_2013():
    dfs_2013 = []
    document_2013 = Document("data/2013 Report survey.docx")
    # print out all columns for categorization

    for paragraph in document_2013.paragraphs:
        if any(run.bold for run in paragraph.runs):
            if not any(substring in paragraph.text for substring in ["Text Entry","View More","%", "Answer"]):
                print(paragraph.text)

def year_2014():
    dfs_2014 = []
    document_2014 = Document("data/2014 System dynamics conference.docx")
    # print out all columns for categorization

    for paragraph in document_2014.paragraphs:
        if any(run.bold for run in paragraph.runs):
            if not any(substring in paragraph.text for substring in ["Text Entry","View More","%", "Answer"]):
                print(paragraph.text)

def year_2015():
    dfs_2015 = []
    document_2015 = Document("data/2015 Report survey.docx")
    # print out all columns for categorization

    for paragraph in document_2015.paragraphs:
        line = paragraph.text
        if re.match(r'^\d+\.\s', line):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split('.', 1)[1]
            print(line)

def year_2016():
    dfs_2016 = []
    document_2016 = Document("data/2016 Report survey.docx")
    # print out all columns for categorization

    for paragraph in document_2016.paragraphs:
        line = paragraph.text
        if line.startswith('Q') and not line.startswith('Qu'):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split(' - ', 1)[1]
            print(line)

def year_2018():
    dfs_2018 = []
    document_2018 = Document("data/2018 ISDC survey report.docx")
    # print out all columns for categorization

    for paragraph in document_2018.paragraphs:
        line = paragraph.text
        if line.startswith('Q'):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split(' - ', 1)[1]
            print(line)


def year_2019():
    dfs_2019 = []
    document_2019 = Document("data/2019 c ISDC.docx")
    # print out all columns for categorization

    for paragraph in document_2019.paragraphs:
        line = paragraph.text
        if line.startswith('Q'):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split(' - ', 1)[1]
            print(line)


def year_2020():
    dfs_2020 = []
    document_2020 = Document("data/2020 ISDC survey Report.docx")
    # print out all columns for categorization

    for paragraph in document_2020.paragraphs:
        line = paragraph.text
        if line.startswith('Q'):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split(' - ', 1)[1]
            print(line)


def year_2021():
    dfs_2021 = []
    document_2021 = Document("data/2021 b ISDC.docx")

    # print out all columns for categorization

    for paragraph in document_2021.paragraphs:
        line = paragraph.text
        if line.startswith('Q'):
            # split at first occurrence of ' - ' and take the part after it
            line = line.split(' - ', 1)[1]
            print(line)

    for table in document_2021.tables:
        text = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(text)
        dfs_2021.append(df)

    print(len(dfs_2021))
    # print("data_type: " + str(type(dfs_2021)))
    # print("data_type item: " + str(type(dfs_2021[0])))
    # print(dfs_2021[0:7])

    # categorical dictionaries
    subset_indices = [0, 1, 25, 26, 27, 28, 29, 35, 36,
                      37, 38, 39, 40]  # Assuming zero-based indexing
    categorical_df_2021 = dfs_2021.iloc[:, subset_indices]
    print(categorical_df_2021.columns)

    slice_1 = dfs_2021[0][3]

    value_counts_dict_1 = {
        "Attend workshops": int(slice_1[1]), "Access session recordings": int(slice_1[2]), "View posters or attend poster session": int(slice_1[3])}

    print(value_counts_dict_1)

    # print(dfs_2021[1])

    # print(dfs_2021[2])

    # boolean dictionaries

    # numerical dictionaries

    # text dictionaries


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
    print(df_2022.head())
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
    print(count_categorical_df_2022.shape)

    count_categorical_df_2022.to_csv("categorical_questions.csv")

    subset_indices = [33, 34, 42, 43]  # Assuming zero-based indexing
    boolean_df_2022 = df_2022.iloc[:, subset_indices]

    # print(boolean_df_2022.head())

    column_names = ["Have you contacted any presenters for more information?",
                    "Did you visit any exhibitors during the conference?",
                    "Would you recommend this event to others?",
                    "Do you plan to attend this conference in the future?"]

    count_boolean_df_2022 = pd.DataFrame(index=["2022"])

    for column_name in column_names:
        bool_counts = boolean_df_2022[column_name].value_counts().to_dict()
        count_boolean_df_2022.loc["2022", column_name] = [bool_counts]

    print(count_boolean_df_2022.shape)
    # print(count_boolean_df_2022)

    count_boolean_df_2022.to_csv("boolean_questions.csv")

    numerical_indices = [2, 4, 6, 8, 10, 12, 13, 14,
                         15, 16, 17, 18, 19, 20, 21, 23]  # Assuming zero-based indexing
    numerical_df_2022 = df_2022.iloc[:, numerical_indices]

    print(numerical_df_2022.columns)
    count_numerical_df_2022 = pd.DataFrame(index=["2022"])

    column_names = ["When it comes to the content of the conference program, my evaluation is:",
                    'When it comes to the conference website and access to presented work, my evaluation is:',
                    'When it comes to the services provided by the conference organization, including technical support, my evaluation is:',
                    'When it comes to the opportunity to socialize at the conference, my evaluation is:',
                    'When it comes to overall conference value, my evaluation is:',
                    'How do you evaluate the following sessions and workshops? [Plenary sessions]',
                    'How do you evaluate the following sessions and workshops? [Parallel sessions]',
                    'How do you evaluate the following sessions and workshops? [Work-in-progress (WIP) sessions]',
                    'How do you evaluate the following sessions and workshops? [Feedback sessions]',
                    'How do you evaluate the following sessions and workshops? [Student-Organized Colloquium on Monday]',
                    'How do you evaluate the following sessions and workshops? [Virtual poster sessions on Wednesday]',
                    'How do you evaluate the following sessions and workshops? [In-presence poster session on Wednessday]',
                    'How do you evaluate the following sessions and workshops? [Roundtables on Friday]',
                    'How do you evaluate the following sessions and workshops? [Online workshops on July 12]',
                    'How do you evaluate the following sessions and workshops? [Hybrid workshops on July 22]',
                    'How do you rate the overall quality of the presented work?']

    for column_name in column_names:
        bool_counts = numerical_df_2022[column_name].value_counts(
        ).to_dict()
        count_numerical_df_2022.loc["2022", column_name] = [bool_counts]

    print(count_numerical_df_2022.shape)
    # print(count_numerical_df_2022)

    count_numerical_df_2022.to_csv("numerical_questions.csv")

    text_indices = [3, 5, 7, 9, 11, 22, 24, 30, 31, 32, 41]
    text_df_2022 = df_2022.iloc[:, text_indices]

    print(text_df_2022.columns)
    # print(text_df_2022["Additional comments"])

    text_responses_2022 = pd.DataFrame(
        index=["2022"], columns=text_df_2022.columns)

    for column_name in text_df_2022.columns:
        # Drop NaN values and convert column to a list
        responses = text_df_2022[column_name].dropna().tolist()
        responses = np.array(responses)
        text_responses_2022.at["2022", column_name] = responses

    print(text_responses_2022.shape)
    print(text_responses_2022)

    text_responses_2022.to_csv("text_responses.csv")


def main():
    # year_2022()
    # year_2021()
    # year_2020()
    # year_2019()
    # year_2018()
    # year_2016()
    # year_2015()
    year_2014()

    # Make big csv from pandas dataframe with year, categorical variables, Q1, Q2, Q19-23, Q26-31, 13 columns
    # Make big csv from pandas dataframe with year, boolean variables, Q24-25, Q32-33, 4 columns
    # Make big csv from pandas dataframe with year, numerical ratings, Q3-18, 16 columns
    # Make big csv from pandas dataframe with year, additional response strings, Addition Qs 1-5, others 11 columns


if __name__ == "__main__":
    main()
