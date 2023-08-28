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

import matplotlib.pyplot as plt
import pandas as pd
import spacy
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud


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

    # Second part: trend analysis

    # Third part: time series cutoff, in person vs hybrid


main()
