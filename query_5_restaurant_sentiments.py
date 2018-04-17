import pandas as pd
import csv
import utils
from textblob import TextBlob


def run_restaurants_sentiments():
    review_file = open("Data/reviews_60601-60606.csv", "r")
    clean_reviews_file = open("Data/clean_reviews_60601-60606.csv", "w")
    review_reader = csv.reader(review_file)
    row_count = len(list(review_reader))
    review_file.seek(0)
    i = 0
    review_writer = csv.writer(clean_reviews_file)
    count = 0
    total_count = 0
    for line in review_reader:
        i += 1
        if len(line) > 10:
            str = line[3]
            initial = 4
            while initial < (len(line) - 6):
                str = str + (line[initial])
                del line[initial]
            line[3] = str
            count = count + 1
        review_writer.writerow(line)
        total_count = total_count + 1
        utils.progress(i, row_count, status='Cleaning reviews dataset')
    clean_reviews_file.close()

    restaurants_file_pd = pd.read_csv("Data/restaurants_60601-60606.csv")
    reviews_file_pd = pd.read_csv("Data/clean_reviews_60601-60606.csv")
    combined_file = pd.merge(restaurants_file_pd, reviews_file_pd, left_on="restaurantID", right_on="restaurantID")
    combined_file.to_csv("Data/restaurants_reviews_combined_file.csv", sep=',', encoding='utf-8')

    combined_file_pd = pd.read_csv("Data/restaurants_reviews_combined_file.csv")

    review_sentiment = []
    end = len(combined_file_pd.index)
    for i in range(end):
        temp = combined_file_pd.ix[i]["reviewContent"]
        blob = TextBlob(temp)
        if blob.sentiment.polarity > 0.175:
            predict_rating = "positive"
        else:
            predict_rating = "negative"
        review_sentiment.append(predict_rating)
        utils.progress(i, end-1, status='Calculating polarity for each review')

    combined_file_pd['Review Sentiment'] = review_sentiment

    result_pd = combined_file_pd[['restaurantID', 'name', 'reviewID', 'Review Sentiment', 'rating_y']]
    result_pd.to_csv("Results/query_5_result.csv")
