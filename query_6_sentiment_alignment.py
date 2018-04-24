import pandas as pd
import utils


def run_sentiment_alignment():
    query_5_result = pd.read_csv("Results/query_5_result.csv")
    user_ratings = query_5_result[['restaurantID', 'rating_y']]
    avg_user_ratings = user_ratings.groupby(['restaurantID']).mean()
    max_sentiment_labels = []
    avg_user_ratings.to_csv("Data/averaged_ratings.csv")
    avg_user_ratings = pd.read_csv("Data/averaged_ratings.csv")

    end = len(avg_user_ratings.index)
    for i in range(end):
        temp1 = query_5_result.loc[(query_5_result['restaurantID'] == avg_user_ratings.iloc[i, 0]) & (query_5_result['Review Sentiment'] == 'positive')]
        temp2 = query_5_result.loc[(query_5_result['restaurantID'] == avg_user_ratings.iloc[i, 0]) & (query_5_result['Review Sentiment'] == 'negative')]
        if len(temp1.index)>len(temp2.index):
            max_sentiment_labels.append('positive')
        else:
            max_sentiment_labels.append('negative')
        utils.progress(i, end-1, status='Assigning sentiment to restaurants')

    avg_user_ratings['average sentiments'] = max_sentiment_labels
    avg_user_ratings.to_csv("Results/query_6_result.csv",index=False)
    print("The output is generated in Results/query_6_result.csv")