import pandas as pd
import re
from difflib import SequenceMatcher
import datetime
import pandasql as psql



biz_data_path = "data/Business_Licenses.csv"
rest_data_path = "data/restaurants_60601-60606.csv"
food_insp_data = "data/Food_Inspections.csv"
out_data_path = "biz_viability.csv"


"""
Utility Functions
"""


def similar(a, b):
    a = a.lower()
    b = b.lower()
    regex = "[^ a-zA-Z0-9]"
    a = re.sub(regex, "", a)
    b = re.sub(regex, "", b)
    return SequenceMatcher(None, a, b).ratio()



"""
Main Functions
"""


def fetch_biz_data():

    df = pd.read_csv(biz_data_path, nrows=50000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[df['BUSINESS_ACTIVITY'].str.lower().str.contains('food', na = False)]
    df = df[['LICENSE_ID', 'DOING_BUSINESS_AS_NAME', 'ADDRESS', 'DATE_ISSUED', 'LICENSE_STATUS',
             'LICENSE_STATUS_CHANGE_DATE', 'ZIP_CODE']]
    df.ZIP_CODE = df.ZIP_CODE.astype(str)
    df = df[df.ZIP_CODE.str.match('6060[0-9]')]
    return df


def fetch_inspection_data():

    df = pd.read_csv(food_insp_data, nrows=500000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['DBA_Name', 'Inspection_ID', 'License_#', 'Address', 'Inspection_Date', 'Results', 'Zip']]
    df = df.rename(columns={'License_#': 'LICENSE_ID', 'DBA_Name':'DOING_BUSINESS_AS_NAME','Address':'ADDRESS'})
    df.Zip = df.Zip.astype(str)
    df = df[df.Zip.str.match('6060[0-9]')]
    df = df[df['Results'].str.lower().str.contains('fail')]

    return df


def generate_biz_viability_report():

    yelp_integrated_frame = fetch_biz_data()
    inspection_data = fetch_inspection_data()
    inspection_data = inspection_data[inspection_data['Results'].str.lower().str.contains('fail')]
    yelp_integrated_frame['DATE_ISSUED'] = pd.to_datetime(yelp_integrated_frame['DATE_ISSUED'], format='%m/%d/%Y')
    yelp_integrated_frame['DATE_ISSUED'] = yelp_integrated_frame['DATE_ISSUED'].dt.date
    yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'] = pd.to_datetime(yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'], format='%m/%d/%Y')
    yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'] = yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'].dt.date
    inspection_data['Inspection_Date'] = pd.to_datetime(inspection_data['Inspection_Date'], format='%m/%d/%Y')
    inspection_data['Inspection_Date'] = inspection_data['Inspection_Date'].dt.date
    inspection_data_test= inspection_data.groupby(['DOING_BUSINESS_AS_NAME', 'ADDRESS'])['Inspection_Date'].max().reset_index()
    yelp_int_test = yelp_integrated_frame.groupby(['DOING_BUSINESS_AS_NAME', 'ADDRESS'])['DATE_ISSUED'].max().reset_index()
    integ = pd.merge(inspection_data_test,yelp_int_test, on=['DOING_BUSINESS_AS_NAME'])
    new_df = pd.DataFrame()

    for dummy,index in integ.iterrows():
        add_x = index['ADDRESS_x']
        add_y = index['ADDRESS_y']
        measure = similar(add_x, add_y)
        if measure >= 0.8 and index['Inspection_Date'].year <= 2014:
            index["diff"] = (index['Inspection_Date'] - index['DATE_ISSUED']).days
            new_df = new_df.append(index)

    new_df = new_df[new_df['diff'] > 750]
    new_df = new_df[['DOING_BUSINESS_AS_NAME','ADDRESS_x','Inspection_Date', 'diff']]
    new_df = new_df.groupby(['DOING_BUSINESS_AS_NAME','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()

    first_issued_lic_data = yelp_integrated_frame.groupby("DOING_BUSINESS_AS_NAME", as_index=False)["DATE_ISSUED"].max()
    yelp_integrated_frame = pd.merge(yelp_integrated_frame,first_issued_lic_data, on=['DOING_BUSINESS_AS_NAME','DOING_BUSINESS_AS_NAME',                                                                                      'DATE_ISSUED','DATE_ISSUED',])
    yelp_integrated_frame = yelp_integrated_frame.drop_duplicates()
    yelp_integrated_frame = yelp_integrated_frame[yelp_integrated_frame['LICENSE_STATUS'].str.lower().str.contains('aac|rev')]

    merged = pd.merge(inspection_data,yelp_integrated_frame, on=['LICENSE_ID'])
    merged['diff'] = 0

    for dummy,index in merged.iterrows():
        merged.at[dummy,"diff"] = (index['LICENSE_STATUS_CHANGE_DATE'] - index['DATE_ISSUED']).days

    merged = merged[['DOING_BUSINESS_AS_NAME_x','ADDRESS_x','Inspection_Date','diff']]
    merged = merged.groupby(['DOING_BUSINESS_AS_NAME_x','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()
    merged = merged.rename(columns={'DOING_BUSINESS_AS_NAME_x': 'DOING_BUSINESS_AS_NAME'})

    final_merge = pd.concat([new_df, merged], ignore_index=True)
    final_merge = final_merge.groupby(['DOING_BUSINESS_AS_NAME','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()
    final_merge['diff'] = final_merge['diff'].apply(lambda x: "{:.2f}".format(float(x)/float(365)))
    final_merge = final_merge.rename(columns={'DOING_BUSINESS_AS_NAME': 'Restaurant Name', 'Inspection_Date':'Failed inspection on','ADDRESS_x':'Address','diff':'Alive for x years'})
    final_merge.to_csv('Results/biz_viability_report.csv', encoding='utf-8', index=False)

    print("Business viability report is Generated with the name biz_viability_report.csv in the Results folder")





generate_biz_viability_report()
