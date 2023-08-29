# We will organize this more detailed analysis into 4 parts

# First, we will use dimensionality reduction and text clustering
# techniques to find pockets of attendees who had similar
# survey responses.

# Second we will carry out sentiment analysis on the text responses to
# see the general tone from each question.

# For text data, we must do this: Sentiment Analysis: Use a sentiment analysis model to
# determine the sentiment of each response. There are several pre-trained models available
# , like the TextBlob library.

# Identify Positive and Negative Responses: Based on the sentiment scores, classify the
# responses into positive, negative, and neutral categories.

# Keyword Extraction: Extract keywords from the positive and negative responses using the
# TF-IDF vectorizer or any other keyword extraction technique.

# Identify Top 5 Things Liked and Disliked: The most frequent keywords in the positive
# responses will give an indication of the things that attendees liked and want to see
# more of, while the most frequent keywords in the negative responses will give an
# indication of the things that attendees disliked and want to change.

from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import ast
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def basic_preprocess_text(text):
    # Remove special characters, numbers, and punctuations
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    return text


def split_into_individual_responses(text):
    responses = [response for sublist in text.values.flatten()
                 for response in sublist]

    individual_responses = [response.split(
        '\n') for response in responses if response]

    individual_responses = [
        item for sublist in individual_responses for item in sublist if item]

    return individual_responses


def analyze_sentiments(data):
    # Flatten the dataframe to get a list of all responses
    individual_responses = split_into_individual_responses(data)

    # Display the first few responses
    print("first few responses: ")
    print(individual_responses[:5])

    # Perform sentiment analysis on the responses
    sentiments = [
        TextBlob(response).sentiment.polarity for response in individual_responses]

    # Classify the responses into positive, negative, and neutral
    positive_responses = [individual_responses[i]
                          for i in range(len(individual_responses)) if sentiments[i] > 0.1]
    negative_responses = [individual_responses[i]
                          for i in range(len(individual_responses)) if sentiments[i] < -0.1]
    neutral_responses = [individual_responses[i] for i in range(
        len(individual_responses)) if sentiments[i] >= -0.1 and sentiments[i] <= 0.1]

    return positive_responses, negative_responses, neutral_responses

# Display the topics


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
              for i in topic.argsort()[:-no_top_words - 1:-1]]))


def get_top_n_representative_responses_for_each_topic(responses, n):
    # Only consider the first 50 words of each response
    responses = [' '.join(response.split()[:50]) for response in responses]

    # Tokenize the text and convert it to bag-of-words representation
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = vectorizer.fit_transform(responses)
    lda = LatentDirichletAllocation(
        n_components=3, max_iter=5, learning_method='online', learning_offset=50., random_state=0).fit(tf)

    # Get topic distribution for each response
    topic_distributions = lda.transform(tf)

    # Get the top N most representative responses for each topic
    most_representative_responses = {}
    for topic_idx in range(topic_distributions.shape[1]):
        top_n_representative_response_idxs = topic_distributions[:, topic_idx].argsort(
        )[-n:]
        most_representative_responses[topic_idx] = [
            responses[i] for i in top_n_representative_response_idxs]

    return most_representative_responses


def extract_keywords(texts, num_keywords=5, ngram=1):
    # Create a TF-IDF Vectorizer object
    vectorizer = TfidfVectorizer(ngram_range=(
        ngram, ngram), stop_words='english')
    # Fit the texts to the vectorizer
    tfidf_matrix = vectorizer.fit_transform(texts)
    # Get the words from the vocabulary
    feature_names = vectorizer.get_feature_names_out()
    # Get the importance of each word
    importance = np.asarray(tfidf_matrix.mean(axis=0)).ravel().tolist()
    # Create a dataframe with the words and their importance
    df = pd.DataFrame({'Term': feature_names, 'Importance': importance})
    # Sort the dataframe by importance
    df = df.sort_values('Importance', ascending=False)
    return df.head(num_keywords)


def main():
    print("starting!!")

    # Part 1: dimensionality reduction and text clustering to generate insights on
    # the survey responses

    # Part 2: sentiment analysis to see the tones per answer

    # Load the data
    file_path = 'text_responses.csv'
    data = pd.read_csv(file_path)

    print("Text Data:" + str(data.head()))

    # # Apply the basic preprocessing to each column of the dataset
    basic_preprocessed_data = data.applymap(
        lambda x: basic_preprocess_text(str(x)) if pd.notna(x) else '')

    basic_preprocessed_data = basic_preprocessed_data.applymap(
        lambda x: ast.literal_eval(str(x)) if '[' in str(x) else [str(x)])

    positive_responses, negative_responses, neutral_responses = analyze_sentiments(
        basic_preprocessed_data)

    print("Overall data sentiment analysis: ")
    print("positive: " + str(len(positive_responses)), "negative: " + str(len(
        negative_responses)), "neutral: " + str(len(neutral_responses)))

    # To do a sanity check, we will look at the sentiment analysis of the responses
    # from the worst and best things that happened to you at the conference

    print("Best thing that happened to you data sentiment analysis: ")

    best_thing = basic_preprocessed_data["What was the best thing that happened to you at the conference?"]
    best_pos_resp, best_neg_resp, best_neu_resp = analyze_sentiments(
        best_thing)

    print("positive: " + str(len(best_pos_resp)), "negative: " + str(len(
        best_neg_resp)), "neutral: " + str(len(best_neu_resp)))

    print("worst thing that happened to you data sentiment analysis: ")

    worst_thing = basic_preprocessed_data["What was the worst thing that happened to you at the conference?"]
    worst_pos_resp, worst_neg_resp, worst_neu_resp = analyze_sentiments(
        worst_thing)

    print("positive: " + str(len(worst_pos_resp)), "negative: " + str(len(
        worst_neg_resp)), "neutral: " + str(len(worst_neu_resp)))

    # Extract keywords with Tf-IDF vectorizer to see what was most mentioned in the positive
    # and negative responses
    # Make a Top 5 list of things liked and disliked.
    positive_keywords = extract_keywords(positive_responses)
    negative_keywords = extract_keywords(negative_responses)

    print("\nOne words: ")
    print(positive_keywords)
    print(negative_keywords)

    positive_bigrams = extract_keywords(positive_responses, ngram=2)
    negative_bigrams = extract_keywords(negative_responses, ngram=2)

    print("\nTwo words: ")
    print(positive_bigrams)
    print(negative_bigrams)

    positive_trigrams = extract_keywords(positive_responses, ngram=3)
    negative_trigrams = extract_keywords(negative_responses, ngram=3)

    print("\nThree words: ")
    print(positive_trigrams)
    print(negative_trigrams)

    # Let's look for phrases instead of just individual terms

    # Extract the most representative answers from the positive and negative responses
    # Get two responses for the three most important categories

    positive_most_representative_responses = get_top_n_representative_responses_for_each_topic(
        positive_responses, 2)
    negative_most_representative_responses = get_top_n_representative_responses_for_each_topic(
        negative_responses, 2)

    print("\n\n\n Most representative repsonses: \n \n ")

    print("Positive most representative responses")
    print(positive_most_representative_responses)

    print("Negative most representative responses")
    print(negative_most_representative_responses)


main()
