import sys
import time
import argparse
import warnings
import query1_crime_report as q1
import query_2_crime_prediction as q2
import query3_crime_stats as q3
import query_4_inspection_result as q4
import query_5_restaurant_sentiments as q5
import query_6_sentiment_alignment as q6
import query_7_predict_review as q7
import query8_biz_viability as q8
import query_9_crime_bl_census_integration as q9
import query_10_crime_weather_predict as q10


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--Query', help='Name of the query(available in list of queries[Readme.txt])', required=True)
    parser.add_argument('-args', '--Arguments', help='Enables additional arguments to the query',required=False)
    #parser.add_argument('-all','--AllQueries', help='It runs all the queries[Input: Y/N]', required=False)
    args = vars(parser.parse_args())

    print("Query is executing....It might take several minutes...")

    if args['Query'] == "query1":
        q1.generate_crime_reports_blocks()
    elif args['Query'] == "query2":
        print(q2.run_crime_prediction(args['Arguments']))
    elif args['Query'] == "query3":
        q3.generate_crime_stats()
    elif args['Query'] == "query4":
        q4.run_food_inspection_result()
    elif args['Query'] == "query5":
        q5.run_restaurants_sentiments()
    elif args['Query'] == "query6":
        q6.run_sentiment_alignment()
    elif args['Query'] == "query7":
        q7.run_predict_review(args['Arguments'])
    elif args['Query'] == "query8":
        q8.generate_biz_viability_report()
    elif args['Query'] == "query9":
        q9.run_crime_extraction_for_census()
    elif args['Query'] == "query10":
        q10.run_crime_weather_predict()
    else:
        print("Invalid Arguments. Please refer the Readme document")


main()







