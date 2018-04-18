import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import naive_bayes
from sklearn import metrics
from sklearn.metrics import classification_report
import utils


def run_predict_review(review_text):
    if review_text is None or review_text == "":
        return
    utils.data_preprocessing()
    df = pd.read_csv("Data/preprocessed_reviews_file.csv", names=['reviewContent', 'rating'])
    stopset = set(stopwords.words('english'))
    vectorizer = TfidfVectorizer(use_idf=True, lowercase=True, strip_accents='ascii', stop_words=stopset)
    y = df['rating']
    X = vectorizer.fit_transform(df.reviewContent)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    clf = naive_bayes.MultinomialNB()
    print("Fitting Multinomial Naive Bayes Classifier")
    clf.fit(X, y)
    # y_pred_class = clf.predict(X_test)
    # print(metrics.accuracy_score(y_test, y_pred_class))
    # confusion = metrics.confusion_matrix(y_test, y_pred_class)
    # TP = []
    # TN = []
    # FP = []
    # FN = []
    # TP.append(confusion[])
    # print(classification_report(X, y))
    Review_input = np.array([review_text])
    Review_input_vector = vectorizer.transform(Review_input)
    print("Predicted review rating: " + str(clf.predict(Review_input_vector)[0]))
    print("Review Content: " + review_text)
