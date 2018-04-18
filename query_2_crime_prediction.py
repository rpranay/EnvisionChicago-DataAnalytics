import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn import tree
from sklearn import linear_model
from sklearn.cross_validation import train_test_split


def run_crime_prediction(block_address):
    if block_address is None or block_address == "":
        print("Invalid address")
        return
    t = block_address
    block_address = block_address.upper()
    useful_cols = ['Male%', 'Female%', 'Median Age', 'block_code']
    crime_data = pd.read_csv("Data/for_crime_classification.csv")

    le_address = LabelEncoder()
    le_crime = LabelEncoder()
    crime_data["block_code"] = le_address.fit_transform(crime_data["Address"])
    male, female, median_age = 0, 0, 0
    try:
        block_address = crime_data[crime_data["Address"] == block_address].block_code[0]
        male = crime_data[crime_data["block_code"] == block_address]["Male%"][0]
        female = crime_data[crime_data["block_code"] == block_address]["Female%"][0]
        median_age = crime_data[crime_data["block_code"] == block_address]["Median Age"][0]
    except IndexError:
        block_address = 0
    except KeyError:
        block_address = 0
    crime_data["pt_code"] = le_crime.fit_transform(crime_data["Crime Type"].fillna('-1'))
    crime_data = crime_data[np.isfinite(crime_data['Male%'])]
    crime_data = crime_data[np.isfinite(crime_data['Female%'])]
    crime_data = crime_data[np.isfinite(crime_data['Median Age'])]
    X = crime_data[useful_cols]
    y = crime_data['pt_code']

    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.3)
    data = [[male, female, median_age, block_address]]
    data_df = pd.DataFrame(data)

    list_stats = [['Address', 'Crime Type', 'Technique', 'Probability']]
    list_stats.append([])
    list_stats.append([])
    list_stats[1].append(t)
    list_stats[2].append(t)

    # Decision tree
    clf = tree.DecisionTreeClassifier()
    print("Fitting Decision Tree model")
    clf = clf.fit(train_x, train_y)
    crime_type = le_crime.inverse_transform(clf.predict(data_df))[0]
    list_stats[1].append(crime_type)
    list_stats[1].append("Decision Tree")
    prob = clf.predict_proba(data_df)
    list_stats[1].append(round(prob.max(), 2))

    #Multinomial Logistic Regression
    print("Fitting Multinomial Logistic Regression model")
    mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)
    crime_type = le_crime.inverse_transform(mul_lr.predict(data_df))[0]
    list_stats[2].append(crime_type)
    list_stats[2].append("Multinomial Logistic Regression")
    prob = mul_lr.predict_proba(data_df)
    list_stats[2].append(round(prob.max(), 2))

    stats_pd = pd.DataFrame(list_stats)
    print(stats_pd)
