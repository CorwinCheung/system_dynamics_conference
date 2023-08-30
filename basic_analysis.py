# We will organize this basic analysis into three parts

# First we will mine the text data for common issues raised by attendees
# and also suggestions that could be implemented. We will use NLP for this

# Second we will analysis trends from the boolean, categorical, and numerical
# question responses to see how attendees viewed parts of the conference
# over time. In more advanced versions of this, we will use time series analysis

# Third we will compare the data before and after the in person/remote/hybrid
# transitions. Using the years when the conference was held fully in person
# versus when the conference was fully remote vs hybrid, we can draw conclusions
# based on the survey responses to see how this affected attendee experience.

import re
from collections import Counter
from ast import literal_eval

import matplotlib.pyplot as plt
import ast
import pandas as pd
import spacy
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud
from scipy.stats import mannwhitneyu


def basic_preprocess_text(text):
    # Remove special characters, numbers, and punctuations
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    return text


def get_lda_topics(vectorizer, lda):
    # Get the top 10 words for each topic
    feature_names = vectorizer.get_feature_names_out()
    top_words_per_topic = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        top_words_per_topic.append(top_words)

    return (top_words_per_topic)


def calculate_weighted_average(rating_dict):
    # Calculate the weighted sum
    total_count = sum(rating_dict.values())
    weighted_sum = sum(k * v for k, v in rating_dict.items())

    # Return the weighted average or None if total_count is 0
    return weighted_sum / total_count if total_count != 0 else None


def extract_numeric_key(key_string):
    numeric_part = re.search(r'\d+', key_string)
    if numeric_part:
        return int(numeric_part.group())
    return 0


def convert_string_to_dict(value):
    if pd.isna(value):
        return {k: 0 for k in range(1, 8)}
    if isinstance(value, str):
        # Handle malformed strings
        value = value.replace("{", "").replace(
            "}", "").replace("'", "").replace('"', '')
        items = value.split(", ")
        return {extract_numeric_key(k): float(v) for k, v in [item.rsplit(": ", 1) for item in items] if extract_numeric_key(k) != 0}
    return {extract_numeric_key(str(k)): v for k, v in value.items() if extract_numeric_key(str(k)) != 0}


def calculate_yes_percentage(response_dict):
    if pd.isna(response_dict):
        return -1
    if isinstance(response_dict, str):
        response_dict = ast.literal_eval(response_dict)
    if response_dict:
        total_responses = sum(response_dict.values())
        yes_responses = response_dict.get('Yes', 0)
        return (yes_responses / total_responses) * 100
    return 0


def safe_eval(cell):
    if isinstance(cell, str):
        return eval(cell)
    else:
        return cell


def calculate_percentage(response_dict):
    if pd.isna(response_dict):
        return {k: 0 for k in range(1, 8)}
    if response_dict:
        total_responses = sum(response_dict.values())
        return {k: (v / total_responses) * 100 for k, v in response_dict.items()}
    return {k: 0 for k in range(1, 8)}


def new_safe_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val


def transform_data(data):
    transformed_data = {}
    for year, responses in data.items():
        transformed_data[year] = []
        for response, count in responses.items():
            if "No opinion" == response:
                continue
            if isinstance(response, int):
                transformed_data[year].extend([response] * count)
            else:
                # Convert the response to an integer (e.g., '7: very positive' to 7)
                response_int = int(response.split(':')[0])
                transformed_data[year].extend([response_int] * count)
    return transformed_data


def main():

    # First part: text data mining

    # Load the data
    file_path = 'text_responses.csv'
    data = pd.read_csv(file_path)

    print("Text Data:" + str(data.head()))

    # Apply the basic preprocessing to each column of the dataset
    basic_preprocessed_data = data.applymap(
        lambda x: basic_preprocess_text(str(x)) if pd.notna(x) else '')

    # Combine all the text data into a list of comments
    comments = basic_preprocessed_data.apply(
        lambda x: ' '.join(x), axis=1).tolist()
    comments = [comment.replace('nmeeting', 'meeting') for comment in comments]
    comments = [comment.replace('ni', 'i') for comment in comments]

    print("Comments:" + str(comments[0]))
    # print the head of comments

    text_corpus = ' '.join(comments)

    # Create and display the word cloud
    # Make a word cloud of most common words in the responses:
    # Specify stop words manually
    stop_words = set([
        'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at',
        'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
        'can', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
        'each', 'few', 'for', 'from', 'further',
        'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's",
        'hers', 'herself', 'him', 'himself', 'his', 'how', "how's",
        'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself',
        "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself',
        'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
        'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such',
        'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
        "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
        'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where',
        "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't",
        'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'aren', 'couldn', 'didn', 'doesn', 'don',
        'hadn', 'hasn', 'haven', 'isn', 'let', 'll', 'mustn', 're', 'shan', 'shouldn', 've', 'wasn', 'weren', 'won', 'wouldn',
    ])

    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          stopwords=stop_words).generate(text_corpus)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # conference_2022 = comments[0]

    # wordcloud = WordCloud(width=800, height=400, background_color='white',
    #                       stopwords=stop_words).generate(conference_2022)
    # plt.figure(figsize=(10, 7))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

    # conference_2021 = comments[1]

    # wordcloud = WordCloud(width=800, height=400, background_color='white',
    #                       stopwords=stop_words).generate(conference_2021)
    # plt.figure(figsize=(10, 7))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

    # conference_2019 = comments[3]

    # wordcloud = WordCloud(width=800, height=400, background_color='white',
    #                       stopwords=stop_words).generate(conference_2019)
    # plt.figure(figsize=(10, 7))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

    # Make a wordcloud for a in person workshop(2019)
    # Make a wordcloud for a virtual workshop(2021)
    # Make a wordcloud for a hybrid workshop(2022)

    # this list now has one comment per row of original data
    # now that we processed the data, we will carry out topic modeling

    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(comments)

    # converts the text data into a numerical format, ignoring words that occur in more than 95% of the comments and less than
    # 2% of the comments, removes english stop words(like: and, the, but, etc.)

    # Fit LDA model, topic modeling: uncover thematic structure in documents.
    # We can fit the model for a number of components(number of topics it will look for)

    # 5
    lda5 = LatentDirichletAllocation(n_components=5, random_state=0)
    lda5.fit(X)

    # print("X:" + str(X))

    top_words_per_topic_5 = get_lda_topics(vectorizer=vectorizer, lda=lda5)
    print("Top words per 5 topics:")
    for i in top_words_per_topic_5:
        print(i)
    print("we can correlate these with these topics:")
    print("1. General Conference Logistics, Attendee Feedback, and Research Topics")
    print("2. Hotel Amenities, Food Options, and Travel Logistics")
    print("3. Virtual Conference Experience and Accessibility")
    print("4. Community Interaction, Networking Opportunities, and Panel Discussions")
    print("5. Research Presentations, Academic Support, and Global Impact")

    print("Since the fourth and fifth categories seem suspect, let's try with 4 components")

    lda4 = LatentDirichletAllocation(n_components=4, random_state=0)
    lda4.fit(X)

    # print("X:" + str(X))

    top_words_per_topic_4 = get_lda_topics(vectorizer=vectorizer, lda=lda4)
    print("Top words per 4 topics:")
    for i in top_words_per_topic_4:
        print(i)
    print("we can correlate these with these topics:")
    print("1. Conference Venue, Accommodation, and Catering")
    print("2. Meals, Location, and Research Networking")
    print("3. Virtual Accessibility, Workshop Experience, and Online Tools")
    print("4. Feedback on Virtual Tools, Support from the Society, and Global Research Impact")
    print("Still, category 3 and 4 seems like they can be combined, let's try with 3 components")

    lda3 = LatentDirichletAllocation(n_components=3, random_state=0)
    lda3.fit(X)
    top_words_per_topic_3 = get_lda_topics(vectorizer=vectorizer, lda=lda3)
    print("Top words per 3 topics:")
    for i in top_words_per_topic_3:
        print(i)

    print("we can correlate these with these topics:")
    print("1. Conference Venue, Catering, and Attendee Feedback")
    print("2. Accommodation, Business Amenities, and Travel Logistics")
    print("3. Virtual Conference Experience and Accessibility")

    # Let's now use Tf-idf in order to see the most popular keywords over each year's responses
    # Term frequency-inverse document frequency measures the combined term frequency and inverse document frequency
    # how important it is to that year specifically versus across the all time text responses

    # Vectorize the text data using TF-IDF vectorizer

    stop_words_list = list(stop_words)

    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95, min_df=2, stop_words=stop_words_list)
    tfidf_matrix = tfidf_vectorizer.fit_transform(comments)

    # Get the updated feature names (words)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Get the top 7 keywords for each response
    top_keywords_per_response = []
    for i in range(tfidf_matrix.shape[0]):
        tfidf_scores = tfidf_matrix[i].toarray()[0]
        top_keywords = [feature_names[j]
                        for j in tfidf_scores.argsort()[:-7 - 1:-1]]

        top_keywords_per_response.append(top_keywords)

    year_labels = [2022, 2021, 2020, 2019, 2018, 2016, 2015, 2014, 2013]

    # Display the year label and top 7 keywords for each response
    for i in range(len(year_labels)):
        print(f"{year_labels[i]}: {top_keywords_per_response[i]}")

    # Let's now use Named Entity Recognition(NER) to extract entities thathave predefined
    # categories like names of people or locations and expressions of time, monetary values, etc.
    # we will use the spaCy model, a open source library trained for this type of NLP

    # Load the spaCy model
    nlp = spacy.load('en_core_web_sm')

    # Process the text data
    docs = [nlp(comment) for comment in comments]

    # Extract named entities, phrases and concepts
    entities = [ent.text for doc in docs for ent in doc.ents]

    # Get the most common entities
    common_entities = Counter(entities).most_common(10)

    # top ten named entities, phrases and concepts
    print(common_entities)

    entities = [ent.text for doc in docs for ent in doc.ents if ent.text.lower() not in
                ['one', 'two', 'three', 'next year', 'the day', 'this year', 'first', 'second', 'last year']]

    # Get the most common entities
    common_entities = Counter(entities).most_common(10)

    print(common_entities)

    # screen out for uninformatived entities

    # # Second part: trend analysis

    # # Numerical trend analysis

    file_path = 'numerical_questions.csv'
    numerical_data = pd.read_csv(file_path)

    # # Rename the column for 'Year'
    numerical_data = numerical_data.rename(columns={'Unnamed: 0': 'Year'})
    years = numerical_data['Year']

    # Plot a graph across years of quantity of survey responses by the first question,
    numerical_data['When it comes to the content of the conference program, my evaluation is:_counts'] = numerical_data[
        'When it comes to the content of the conference program, my evaluation is:'].apply(lambda x: ast.literal_eval(str(x)) if pd.notna(x) else {})

    # Replace each dictionary with the sum of its values
    numerical_data['Response_Counts'] = numerical_data[
        'When it comes to the content of the conference program, my evaluation is:_counts'].apply(lambda x: sum(x.values()) if x else 0)

    # Group by 'Year' and sum the total responses
    response_counts = numerical_data.groupby('Year')['Response_Counts'].sum()

    response_year = response_counts.index

    plt.figure(figsize=(10, 6))
    plt.plot(response_year, response_counts, marker='o', color='b')
    plt.xlabel('Year')
    plt.ylabel('Number of Responses')
    plt.title('Quantity of Survey Responses by Year')
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Looking at overall conference value and quality of presented work

    # columns_to_process = [
    #     col for col in numerical_data.columns if col != 'Year']

    columns_to_process = ["When it comes to overall conference value, my evaluation is:",
                          "When it comes to the content of the conference program, my evaluation is:"]

    for column in columns_to_process:
        numerical_data[column] = numerical_data[column].apply(
            convert_string_to_dict)
        numerical_data[column +
                       '_Avg'] = numerical_data[column].apply(calculate_weighted_average)

    numerical_data['Overall_Conference_Value_Avg'] = numerical_data['When it comes to overall conference value, my evaluation is:_Avg']
    numerical_data['Quality_Presented_Work_Avg'] = numerical_data[
        'When it comes to the content of the conference program, my evaluation is:_Avg']

    # Calculate average of calculated weighted averages
    overall_value_avg = numerical_data['Overall_Conference_Value_Avg'].mean()
    quality_presented_work_avg = numerical_data['Quality_Presented_Work_Avg'].mean(
    )

    # Print the calculated averages
    # print("Average Overall Conference Value:", overall_value_avg)
    # print("Average Quality of Presented Work:", quality_presented_work_avg)

    # Create a line plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, numerical_data['Overall_Conference_Value_Avg'],
             marker='o', label='Overall Conference Value')
    plt.plot(years, numerical_data['Quality_Presented_Work_Avg'],
             marker='o', label='Quality of Presented Work')
    plt.axhline(y=overall_value_avg, color='r', linestyle='--',
                label='Average Overall Conference Value')
    plt.axhline(y=quality_presented_work_avg, color='g',
                linestyle='--', label='Average Quality of Presented Work')
    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title(
        'Average Ratings of Conference Value and Presented Work Over the Years')
    plt.legend()
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()

    # Looking at Services provided, Socialization, Location
    # Look at Venue, Fee, Overnight accomadations
    # Looking at Types of sessions, plenary, parallel, WIP,

    columns_and_info = [
        {
            'columns': ["When it comes to the services provided by the conference organization, including technical support, my evaluation is:",
                        "When it comes to the opportunity to socialize at the conference, my evaluation is:",
                        "When it comes to conference geographical location my evaluation is:"],
            'labels': ['Quality of Services Provided', 'Quality of Socialization Opportunities', 'Rating of Location'],
            'colors': ['r', 'g', 'b'],
            'title': 'Average Rating Trends of Meta Statistics Over the Years'
        },
        {
            'columns': ["When it comes to the conference venue (building and facilities) my evaluation is:",
                        "When it comes to the conference fee my evaluation is:",
                        "When it comes to the overnight accommodation my evaluation is:"],
            'labels': ['Quality of Venue', 'Rating of Conference Fee', 'Rating of Overnight Accommodations'],
            'colors': ['r', 'g', 'b'],
            'title': 'Average Rating Trends of Meta Statistics (2) Over the Years'
        },
        {
            'columns': ["How do you evaluate the following sessions and workshops? [Plenary sessions]",
                        "How do you evaluate the following sessions and workshops? [Parallel sessions]",
                        "How do you evaluate the following sessions and workshops? [Work-in-progress (WIP) sessions]"],
            'labels': ['Quality of Plenary Sessions', 'Rating of Parallel Sessions', 'Rating of WIP(Work-in-progress) Sessions'],
            'colors': ['r', 'g', 'b'],
            'title': 'Average Rating Trends of Types of Sessions Over the Years'
        }
    ]

    for group in columns_and_info:
        columns_to_process = group['columns']
        labels = group['labels']
        colors = group['colors']
        title = group['title']

        # Process each column and plot the data
        plt.figure(figsize=(10, 6))

        for i, column in enumerate(columns_to_process):
            label = labels[i]
            color = colors[i]

            # Convert and calculate weighted averages
            numerical_data[column] = numerical_data[column].apply(
                convert_string_to_dict)
            numerical_data[column + '_Avg'] = numerical_data[column].apply(
                calculate_weighted_average)

            # Calculate the overall average
            overall_avg = numerical_data[column + '_Avg'].mean()

            # Plot the data and average line
            plt.plot(years, numerical_data[column + '_Avg'],
                     marker='o', label=label, color=color)
            plt.axhline(y=overall_avg, linestyle='--',
                        label=f'Average {label}', color=color)

        plt.xlabel('Year')
        plt.ylabel('Rating')
        plt.title(title)
        plt.legend()
        plt.xticks(years)
        plt.grid(True)
        plt.tight_layout()

        # Display the plot
        plt.show()
    # Looking at feedback, SOC, Virtual poster, in person poster,
    #

    columns_and_info = [
        {
            'column': "How do you evaluate the following sessions and workshops? [Feedback sessions]",
            'label': 'Rating of Feedback Sessions',
            'color': 'r'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [Student-Organized Colloquium]",
            'label': 'Rating of Student-Organized Colloquium',
            'color': 'g'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [Virtual poster sessions]",
            'label': 'Rating of Virtual Poster Sessions',
            'color': 'b'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [In-presence poster session]",
            'label': 'Rating of In-Presence Poster Sessions',
            'color': 'y'
        }
    ]

    plt.figure(figsize=(10, 6))

    for info in columns_and_info:
        column = info['column']
        label = info['label']
        color = info['color']

        # Convert and calculate weighted averages
        numerical_data[column] = numerical_data[column].apply(
            convert_string_to_dict)
        numerical_data[column + '_Avg'] = numerical_data[column].apply(
            calculate_weighted_average)

        # Calculate the overall average
        overall_avg = numerical_data[column + '_Avg'].mean()

        # Plot the data and average line
        plt.plot(years, numerical_data[column + '_Avg'],
                 marker='o', label=label, color=color)
        plt.axhline(y=overall_avg, linestyle='--',
                    label=f'Average {label}', color=color)

    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title('Average Rating Trends of Types of Sessions (2) Over the Years')
    plt.legend()
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()

    # Looking at roundtables, Online workshops, hybrid workshops Dialog sessions

    # Define the necessary columns and information again
    columns_and_info = [
        {
            'column': "How do you evaluate the following sessions and workshops? [Roundtables]",
            'label': 'Rating of Roundtables',
            'color': 'r'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [Online workshops]",
            'label': 'Rating of Online Workshops',
            'color': 'g'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [Hybrid workshops]",
            'label': 'Rating of Hybrid Workshops',
            'color': 'b'
        },
        {
            'column': "How do you evaluate the following sessions and workshops? [Dialog sessions]",
            'label': 'Rating of Dialog Sessions',
            'color': 'y'
        }
    ]

    # Create a line plot
    plt.figure(figsize=(10, 6))

    # Process each column and plot the data
    for info in columns_and_info:
        column = info['column']
        label = info['label']
        color = info['color']

        # Convert and calculate weighted averages
        numerical_data[column] = numerical_data[column].apply(
            convert_string_to_dict)
        numerical_data[column + '_Avg'] = numerical_data[column].apply(
            calculate_weighted_average)

        # Calculate the overall average
        overall_avg = numerical_data[column + '_Avg'].mean()

        # Plot the data and average line
        plt.plot(years, numerical_data[column + '_Avg'],
                 marker='o', label=label, color=color)
        plt.axhline(y=overall_avg, linestyle='--',
                    label=f'Average {label}', color=color)

    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title(
        'Average Rating Trends of Types of Sessions (3) Over the Years')
    plt.legend()
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()

    # Looking at plenary and parallel sessions, too short or too long, more or less

    # Define the necessary columns and information again
    columns_and_info = [
        {
            'column': "Are the plenary sessions too short or too long?",
            'label': 'Plenary Sessions Duration',
            'color': 'r'
        },
        {
            'column': "Should we have more or fewer plenary sessions?",
            'label': 'Number of Plenary Sessions',
            'color': 'g'
        },
        {
            'column': "Are the parallel sessions too short or too long?",
            'label': 'Parallel Sessions Duration',
            'color': 'b'
        },
        {
            'column': "Should we have more or fewer parallel sessions?",
            'label': 'Number of Parallel Sessions',
            'color': 'y'
        }
    ]

    # Create a line plot
    plt.figure(figsize=(10, 6))

    # Process each column and plot the data
    for info in columns_and_info:
        column = info['column']
        label = info['label']
        color = info['color']

        # Convert and calculate weighted averages
        numerical_data[column] = numerical_data[column].apply(
            convert_string_to_dict)
        numerical_data[column + '_Avg'] = numerical_data[column].apply(
            calculate_weighted_average)

        # Calculate the overall average
        overall_avg = numerical_data[column + '_Avg'].mean()

        # Plot the data and average line
        plt.plot(years, numerical_data[column + '_Avg'],
                 marker='o', label=label, color=color)
        plt.axhline(y=overall_avg, linestyle='--',
                    label=f'Average {label}', color=color)

    plt.xlabel('Year')
    plt.ylabel('Shorter/Fewer(1) to Longer/More(7)')
    plt.title(
        'Average Rating Parallel and Plenary Session Durations and Value Over the Years')
    plt.legend()
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()

    # Looking at breaks, academic work, workshop satisifaction

    # Define the necessary columns and information again
    columns_and_info = [
        {
            'column': "What is your opinion about the duration of the breaks during the conference?",
            'label': 'Duration of Breaks(7 = breaks are too long)',
            'color': 'r'
        },
        {
            'column': "Would you like to see more or less academic work (as compared to applications)?",
            'label': 'Preference for Academic Work vs Applications(7 = more academic work)',
            'color': 'g'
        },
        {
            'column': "How satisfied are you with the workshops?",
            'label': 'Satisfaction with Workshops',
            'color': 'b'
        }
    ]

    # Create a line plot
    plt.figure(figsize=(10, 6))

    # Process each column and plot the data
    for info in columns_and_info:
        column = info['column']
        label = info['label']
        color = info['color']

        # Convert and calculate weighted averages
        numerical_data[column] = numerical_data[column].apply(
            convert_string_to_dict)
        numerical_data[column + '_Avg'] = numerical_data[column].apply(
            calculate_weighted_average)

        # Calculate the overall average
        overall_avg = numerical_data[column + '_Avg'].mean()

        # Plot the data and average line
        plt.plot(years, numerical_data[column + '_Avg'],
                 marker='o', label=label, color=color)
        plt.axhline(y=overall_avg, linestyle='--',
                    label=f'Average {label}', color=color)

    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title('Average Rating Trends of Breaks, Academic Work vs Applications, and Workshops Satisfaction Over the Years')
    plt.legend()
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()

    categorical_data = pd.read_csv('categorical_questions.csv', index_col=0)

    interested_columns = ["How many years of experience do you have with system dynamics?",
                          "Have you attended the SD conference before?",
                          "What is your profession? Please select all that apply.",
                          "What are your fields of interest? Please select all that apply.",
                          "What is your geographic region?"]

    for column in interested_columns:
        categorical_data[column] = categorical_data[column].apply(safe_eval)
        categorical_data[column +
                         '_Percentage'] = categorical_data[column].apply(calculate_percentage)

        plt.figure(figsize=(10, 6))
        for response_option in categorical_data[column + '_Percentage'].iloc[0].keys():
            percentages = [x[response_option]
                           for x in categorical_data[column + '_Percentage'] if x[response_option] != 0]
            plt.plot(categorical_data.index[categorical_data[column +
                                                             '_Percentage'].apply(lambda x: x[response_option] != 0)],
                     percentages,
                     marker='o', label=response_option)

        plt.xlabel('Year')
        plt.ylabel('Percentage (%)')
        plt.title(f'Percentage of Responses for "{column}" Over the Years')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()

    # boolean trend analysis

    boolean_data = pd.read_csv('boolean_questions.csv', index_col=0)

    plt.figure(figsize=(10, 6))
    for i, column in enumerate(boolean_data.columns):
        boolean_data[column] = boolean_data[column].apply(safe_eval)
        boolean_data[column +
                     '_Percentage'] = boolean_data[column].apply(calculate_yes_percentage)
        # Filter out -1 values
        valid_indices = boolean_data[column + '_Percentage'] != -1
        plt.plot(boolean_data.index[valid_indices],
                 boolean_data[column + '_Percentage'][valid_indices], marker='o', label=column)

    plt.xlabel('Year')
    plt.ylabel('Percentage of Yes Responses (%)')
    plt.title('Percentage of Yes Responses Over the Years')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Third part: time series cutoff, in person vs virtual

    # Looking at rows 2020(virtual) and 2019(in person) and comparing between questions that were asking in both

    # Numerical Questions that were asked in both

    numerical_columns = ["When it comes to the content of the conference program, my evaluation is:",
                         "When it comes to the services provided by the conference organization, including technical support, my evaluation is:",
                         "When it comes to the opportunity to socialize at the conference, my evaluation is:",
                         "When it comes to overall conference value, my evaluation is:",
                         "How do you evaluate the following sessions and workshops? [Work-in-progress (WIP) sessions]",
                         "How do you evaluate the following sessions and workshops? [Feedback sessions]",
                         "How do you rate the overall quality of the presented work?",
                         ]

    filtered_data = numerical_data.loc[numerical_data['Year'].isin(
        [2019, 2020]), numerical_columns]

    for column in numerical_columns:
        filtered_data[column] = filtered_data[column].apply(new_safe_eval)

    # Transform the data
    transformed_data = {column: transform_data(
        filtered_data[column]) for column in numerical_columns}

    # print(transformed_data)

    # Perform the Mann-Whitney U test
    p_values = {}
    for column, data in transformed_data.items():
        stat, p = mannwhitneyu(data[2], data[3], alternative='two-sided')
        p_values[column] = p

    for key, value in p_values.items():
        print(f"{key}: {value}")

    # Significant differences are in Opportunities to socialize(went down), services
    # including techical support(went up), and overall quality of presented work(went up)

    numerical_columns = ["When it comes to the content of the conference program, my evaluation is:",
                         "When it comes to the conference website and access to presented work, my evaluation is:",
                         "When it comes to the services provided by the conference organization, including technical support, my evaluation is:",
                         "When it comes to the opportunity to socialize at the conference, my evaluation is:",
                         "When it comes to overall conference value, my evaluation is:",
                         "How do you evaluate the following sessions and workshops? [Plenary sessions]",
                         "How do you evaluate the following sessions and workshops? [Parallel sessions]",
                         "How do you evaluate the following sessions and workshops? [Work-in-progress (WIP) sessions]",
                         "How do you evaluate the following sessions and workshops? [Feedback sessions]",
                         "How do you evaluate the following sessions and workshops? [Student-Organized Colloquium]",
                         "How do you evaluate the following sessions and workshops? [Virtual poster sessions]",
                         "How do you evaluate the following sessions and workshops? [Online workshops]",
                         "How do you rate the overall quality of the presented work?",
                         ]

    filtered_data = numerical_data.loc[numerical_data['Year'].isin(
        [2021, 2022]), numerical_columns]

    for column in numerical_columns:
        filtered_data[column] = filtered_data[column].apply(new_safe_eval)

    # Transform the data
    transformed_data = {column: transform_data(
        filtered_data[column]) for column in numerical_columns}

    # print(transformed_data)

    # Perform the Mann-Whitney U test
    p_values = {}
    for column, data in transformed_data.items():
        stat, p = mannwhitneyu(data[0], data[1], alternative='two-sided')
        p_values[column] = p

    for key, value in p_values.items():
        print(f"{key}: {value}")

    # Significant: Opportunity to socialize at conference: 0.03214420226557648(Went up)


main()
