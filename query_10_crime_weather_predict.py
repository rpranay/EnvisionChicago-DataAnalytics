import pandas as pd
from sklearn import naive_bayes
from sklearn.preprocessing import LabelEncoder

def run_crime_weather_predict():
    df1=pd.read_csv("Data/Zip_Tract.csv")
    df2=pd.read_csv("Data/CensusBlockTIGER2010.csv")
    df3=pd.read_csv("Data/WeatherData.csv")

    df4 = pd.merge(df1, df2,on=['TRACTCE10'])
    df4=df4[['tract_block','Zip']]

    df5 = pd.merge(df4, df3,on=['Zip'])
    df5=df5[['tract_block','Year','month','MeanTemperature']]

    df6=pd.read_csv("Data/Crime_Census_Integrated.csv")
    df6=df6[['Primary Type','tract_block']]
    df7 = pd.merge(df5, df6,on=['tract_block'])

    le_crime = LabelEncoder()
    df7["pt_code"] = le_crime.fit_transform(df7["Primary Type"].fillna('-1'))
    X=df7[['tract_block','Year','month','MeanTemperature']]
    y=df7[['pt_code']]

    clf=naive_bayes.MultinomialNB()
    clf.fit(X, y)


    #Change the below entries with desired values for prediction
    test_X1=[[2517001040,2018,5,35]]
    test_X2=[[7001002031,2019,6,23]]
    test_X3=[[8387002003,2018,3,38]]

    crime_type1 = le_crime.inverse_transform(clf.predict(test_X1))[0]
    prob1 = clf.predict_proba(test_X1)

    crime_type2 = le_crime.inverse_transform(clf.predict(test_X2))[0]
    prob2 = clf.predict_proba(test_X2)


    crime_type3 = le_crime.inverse_transform(clf.predict(test_X3))[0]
    prob3 = clf.predict_proba(test_X3)

    data = []
    data.append(["Tract Block","Year","month","Mean Temperature","Primary Type","Probability"])
    # data.append([])
    data.append([test_X1[0][0],test_X1[0][1],test_X1[0][2],test_X1[0][3],crime_type1,prob1])
    # data.append([])
    data.append([test_X2[0][0],test_X2[0][1],test_X2[0][2],test_X2[0][3],crime_type2,prob2])
    # data.append([])
    data.append([test_X3[0][0],test_X3[0][1],test_X3[0][2],test_X3[0][3],crime_type3,prob3])
    finaldf=pd.DataFrame(data)
    finaldf.to_csv("Results/query_10_result.csv",index=False)
    print("Crime and Weather statistics are generated with the name query_10_result.csv in the results folder")