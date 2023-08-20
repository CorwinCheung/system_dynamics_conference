import os
import pandas as pd
from docx import Document
import numpy as np
import re

cur_path = os.path.dirname(__file__)
true_path = "/Users/corwincheung/Programming/Systems Dynamics Analysis/data"


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


def year_2013():
    dfs_2013 = []
    document_2013 = Document("data/2013 Report survey.docx")
    # print out all columns for categorization

    for paragraph in document_2013.paragraphs:
        if any(run.bold for run in paragraph.runs):
            if not any(substring in paragraph.text for substring in ["Text Entry", "View More", "%", "Answer"]):
                print(paragraph.text)


def year_2014():
    dfs_2014 = []
    document_2014 = Document("data/2014 System dynamics conference.docx")
    # print out all columns for categorization

    for paragraph in document_2014.paragraphs:
        if any(run.bold for run in paragraph.runs):
            if not any(substring in paragraph.text for substring in ["Text Entry", "View More", "%", "Answer"]):
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

    # for paragraph in document_2021.paragraphs:
    #     line = paragraph.text
    #     if line.startswith('Q'):
    #         # split at first occurrence of ' - ' and take the part after it
    #         line = line.split(' - ', 1)[1]
    #         print(line)

    for table in document_2021.tables:
        text = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(text)
        dfs_2021.append(df)

    print(len(dfs_2021))
    print(type(dfs_2021))

    print(type(dfs_2021[0]))

    # print("data_type: " + str(type(dfs_2021)))
    # print("data_type item: " + str(type(dfs_2021[0])))
    # print(dfs_2021[0:7])

    # categorical dictionaries

    # slice_1 = dfs_2021[0][3]

    # value_counts_dict_1 = {
    #     "Attend workshops": int(slice_1[1]), "Access session recordings": int(slice_1[2]), "View posters or attend poster session": int(slice_1[3])}

    # # manual counting for ugly text data

    # value_counts_dict_2 = {
    #     'More than 20 years': 15, '10 to 20 years': 11, '2 years': 9, '3 years': 9,
    #     '1 year or less': 4, '5 to 10 years': 4, '4 years': 2
    # }

    # slice_3 = (dfs_2021[38][3])

    # value_counts_dict_3 = {
    #     'yes, 6 or more times': int(slice_3[4]), 'yes, 2-5 times': int(slice_3[3]), 'no, this was my first time attending the conference': int(slice_3[1]), 'yes, once before': int(slice_3[2])
    # }

    # slice_4 = dfs_2021[40][3]
    # slice_4b = dfs_2021[40][1]

    # value_counts_dict_4 = {
    #     slice_4b[1]: int(slice_4[1]), slice_4b[2]: int(slice_4[2]), slice_4b[3]: int(slice_4[3])
    # }

    # slice_5 = dfs_2021[41][3]
    # slice_5b = dfs_2021[41][1]

    # value_counts_dict_5 = {
    #     slice_5b[1]: int(slice_5[1]), slice_5b[2]: int(slice_5[2]), slice_5b[3]: int(slice_5[3]), slice_5b[4]: int(slice_5[4]), slice_5b[5]: int(slice_5[5])
    # }

    # slice_6 = dfs_2021[50][3]
    # slice_6b = dfs_2021[50][1]

    # value_counts_dict_6 = {
    #     slice_6b[1]: int(slice_6[1]), slice_6b[2]: int(slice_6[2]), slice_6b[3]: int(slice_6[3]), slice_6b[4]: int(slice_6[4]),
    #     slice_6b[5]: int(slice_6[5]), slice_6b[6]: int(slice_6[6]), slice_6b[7]: int(slice_6[7]), slice_6b[8]: int(slice_6[8]),
    #     slice_6b[9]: int(slice_6[9]),
    # }

    # slice_7 = dfs_2021[52][3]
    # slice_7b = dfs_2021[52][1]

    # value_counts_dict_7 = {
    #     slice_7b[1]: int(slice_7[1]), slice_7b[2]: int(slice_7[2]), slice_7b[3]: int(slice_7[3]), slice_7b[4]: int(slice_7[4]),
    #     slice_7b[5]: int(slice_7[5]), slice_7b[6]: int(slice_7[6]), slice_7b[7]: int(slice_7[7]), slice_7b[8]: int(slice_7[8]),
    #     slice_7b[9]: int(slice_7[9]), slice_7b[10]: int(slice_7[10]), slice_7b[11]: int(slice_7[11]), slice_7b[12]: int(slice_7[12]),
    #     slice_7b[13]: int(slice_7[13]), slice_7b[14]: int(slice_7[14])
    # }

    # slice_8 = dfs_2021[55][3]
    # slice_8b = dfs_2021[55][1]

    # value_counts_dict_8 = {
    #     slice_8b[1]: int(slice_8[1]), slice_8b[2]: int(slice_8[2]), slice_8b[3]: int(slice_8[3]), slice_8b[4]: int(slice_8[4]),
    #     slice_8b[5]: int(slice_8[5]), slice_8b[6]: int(slice_8[6])
    # }

    # slice_9 = dfs_2021[63][3]
    # slice_9b = dfs_2021[63][1]

    # value_counts_dict_9 = {
    #     slice_9b[1]: int(slice_9[1]), slice_9b[2]: int(slice_9[2]), slice_9b[3]: int(slice_9[3])
    # }

    # print(value_counts_dict_9)

    # dicts = [value_counts_dict_1, value_counts_dict_2, value_counts_dict_3, value_counts_dict_4,
    #          value_counts_dict_5, value_counts_dict_6, value_counts_dict_7, value_counts_dict_8,
    #          value_counts_dict_9]

    # for i, d in enumerate(dicts):
    #     dicts[i] = {k: v for k, v in sorted(
    #         d.items(), key=lambda item: item[1], reverse=True)}

    # value_counts_dict_1, value_counts_dict_2, value_counts_dict_3, value_counts_dict_4, value_counts_dict_5, value_counts_dict_6, value_counts_dict_7, value_counts_dict_8, value_counts_dict_9 = dicts

    # value_counts_dicts = {
    #     "What aspects of the virtual conference did you experience? Select all that apply.": value_counts_dict_1,
    #     "How many years of experience do you have with system dynamics?": value_counts_dict_2,
    #     "Have you attended the SD conference before?": value_counts_dict_3,
    #     "How do you evaluate this year’s hybrid format as compared to the purely in presence and virtual formats?": value_counts_dict_4,
    #     "Which of the following features, if any, would be worthwhile to continue for future conferences? Please select all that apply.": value_counts_dict_5,
    #     "What is your profession? Please select all that apply.": value_counts_dict_6,
    #     "What are your fields of interest? Please select all that apply.": value_counts_dict_7,
    #     "What is your geographic region?": value_counts_dict_8,
    #     "The next conference is likely to be a hybrid (virtual and in-person) event. In which way would you prefer to attend?": value_counts_dict_9,
    # }

    # # print(value_counts_dicts)

    # df = pd.read_csv("categorical_questions.csv", index_col=0)

    # if '2021' not in df.index:
    #     df.loc['2021'] = pd.NA

    # for col_name, col_data in value_counts_dicts.items():
    #     if col_name in df.columns:
    #         df.at['2021', col_name] = col_data  # assuming year is the index
    #     else:
    #         # Add a new column with NaN for all previous rows
    #         df[col_name] = pd.NA
    #         df.at['2021', col_name] = col_data

    # df.to_csv("categorical_questions.csv")

    # print(dfs_2021[1])

    # print(dfs_2021[2])

    # boolean dictionaries

    # print(dfs_2021[47])

    # slice_10 = dfs_2021[47][3]

    # value_counts_dict_10 = {
    #     'Yes': int(slice_10[1]), 'No': int(slice_10[2])
    # }

    # slice_11 = dfs_2021[49][3]

    # value_counts_dict_11 = {
    #     'Yes': int(slice_11[1]), 'No': int(slice_11[2])
    # }

    # slice_12 = dfs_2021[59][3]

    # value_counts_dict_12 = {
    #     'Yes': int(slice_12[1]), 'No': int(slice_12[2])
    # }

    # slice_13 = dfs_2021[61][3]

    # value_counts_dict_13 = {
    #     'Yes': int(slice_13[1]), 'No': int(slice_13[2])
    # }

    # # print(value_counts_dict_13)

    # boolean_value_counts_dicts = {
    #     "Have you contacted any presenters for more information?": value_counts_dict_10,
    #     "Did you visit any exhibitors during the conference?": value_counts_dict_11,
    #     "Would you recommend this event to others?": value_counts_dict_12,
    #     "Do you plan to attend this conference in the future?": value_counts_dict_13,
    # }

    # print(boolean_value_counts_dicts)

    # df = pd.read_csv("boolean_questions.csv", index_col=0)

    # if '2021' not in df.index:
    #     df.loc['2021'] = pd.NA

    # for col_name, col_data in boolean_value_counts_dicts.items():
    #     if col_name in df.columns:
    #         df.at['2021', col_name] = col_data  # assuming year is the index
    #     else:
    #         # Add a new column with NaN for all previous rows
    #         df[col_name] = pd.NA
    #         df.at['2021', col_name] = col_data

    # df.to_csv("boolean_questions.csv")

    # numerical dictionaries

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

    boolean_value_counts_dicts = {
        "When it comes to the content of the conference program, my evaluation is:": value_counts_dict_14,
        "When it comes to the conference website and access to presented work, my evaluation is:": value_counts_dict_15,
        "When it comes to the services provided by the conference organization, including technical support, my evaluation is:": value_counts_dict_16,
        "When it comes to the opportunity to socialize at the conference, my evaluation is:": value_counts_dict_17,
        "When it comes to overall value, my evaluation is:": value_counts_dict_18,
        "When it comes to the plenary sessions, my evaluation is:": value_counts_dict_19,
        "When it comes to the parallel sessions, my evaluation is:": value_counts_dict_20,
        "When it comes to the work-in-progress (WIP) sessions, my evaluation is:": value_counts_dict_21,
        "When it comes to the dialog sessions, my evaluation is:": value_counts_dict_22,
        "When it comes to the feedback sessions, my evaluation is:": value_counts_dict_23,
        "When it comes to the Student-organized Colloquium on Sunday, my evaluation is:": value_counts_dict_24,
        "When it comes to the poster sessions on Tuesday, my evaluation is:": value_counts_dict_25,
        "When it comes to the workshops on Thursday and Friday, my evaluation is:": value_counts_dict_26,
        "How do you rate the overall quality of the presented work?": value_counts_dict_27,
    }

    # text dictionaries


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
    year_2021()
    # year_2020()
    # year_2019()
    # year_2018()
    # year_2016()
    # year_2015()
    # year_2014()

    # Make big csv from pandas dataframe with year, categorical variables, Q1, Q2, Q19-23, Q26-31, 13 columns
    # Make big csv from pandas dataframe with year, boolean variables, Q24-25, Q32-33, 4 columns
    # Make big csv from pandas dataframe with year, numerical ratings, Q3-18, 16 columns
    # Make big csv from pandas dataframe with year, additional response strings, Addition Qs 1-5, others 11 columns


if __name__ == "__main__":
    main()
