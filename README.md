# system_dynamics_conference

Analyzing the International Society of System Dynamics yearly conference survey data.

CSV, Docx, and xlsx files are not uploaded to retain the privacy of the surveyees

Please contact corwincheung@college.harvard.edu for the data to reproduce these findings and run the code.

Run preprocessing.py to create the csvs for each of the question types across 10 years: boolean, categorical, numerical, and text

Then run basic_analysis.py to generate the reports for the basic analysis carried out.

Then run detailed_analysis.py to generate the more detailed parts of the reports: time series analysis, statistical significance testing, advanced trends, semantic analysis on text data, and text response clustering.

run "python -m spacy download en_core_web_sm" before running basic_analysis.py if you get an import error
