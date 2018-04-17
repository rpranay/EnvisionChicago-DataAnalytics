import pandas as pd


crimes_data_path = "data/Crimes.csv"
rest_biz_integrated_data_path = "data/Restaurant_Biz_Match.csv"


def fetch_crimes():
    df = pd.read_csv(crimes_data_path, nrows=5000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['Block','Primary_Type','Arrest','Year','Latitude','Longitude']]
    df['Block'] = df["Block"].apply(lambda x: x.lower())
    df = pd.DataFrame({'ArrestCount': df.groupby(['Block','Primary_Type','Year','Arrest','Latitude','Longitude']).size()}).reset_index()
    df.loc[df['Arrest'] == False, 'ArrestCount'] = 0
    return df


def fetch_rest_biz_integrated():
    df = pd.read_csv(rest_biz_integrated_data_path, nrows=5000)
    return df


def generate_crime_reports_blocks():

    new_df = fetch_rest_biz_integrated()
    crime_frame = fetch_crimes()
    final_frame = pd.DataFrame()
    rest_names = new_df['name'].unique()
    rest_names = rest_names.tolist()

    for restaurant in rest_names:

        temp_rest_data = new_df[new_df['name'] == restaurant]
        check_license = temp_rest_data[temp_rest_data['licence_description'].str.contains("Liquor")].size > 0
        check_license1 = temp_rest_data[temp_rest_data['licence_description'].str.contains("Tobacco")].size > 0
        temp_rest_data = temp_rest_data.iloc[0]
        temp_rest_data['has_liqour_license'] = check_license
        temp_rest_data['has_Tobacco_license'] = check_license1
        temp_crime_frame = crime_frame[crime_frame['Block'] == temp_rest_data['Block']]

        if temp_crime_frame.size > 0:

            lat = temp_crime_frame.iloc[0]['Latitude']
            long = temp_crime_frame.iloc[0]['Longitude']
            maxLat = lat + 0.003
            minLat = lat - 0.003
            maxLong = long + 0.003
            minLong = long - 0.003
            blocks_3_crimes = crime_frame[(crime_frame['Latitude'] >= minLat) & (crime_frame['Latitude'] <= maxLat) & (
                        crime_frame['Longitude'] <= minLong) & (crime_frame['Longitude'] <= maxLong)]
            if blocks_3_crimes.size > 0:

                blocks_3_crimes1 = pd.DataFrame(
                    {'total': blocks_3_crimes.groupby(["Primary_Type", "Year"]).size()}).reset_index()
                blocks_3_crimes = blocks_3_crimes.groupby(['Primary_Type', 'Year'], as_index=False)[
                    ["ArrestCount"]].sum()
                blocks_3_crimes = pd.merge(blocks_3_crimes, blocks_3_crimes1, on=['Primary_Type', 'Year'])
                on_prem_crimes = crime_frame[crime_frame['Block'] == temp_rest_data['Block']]

                if on_prem_crimes.size > 0:

                    on_prem_crimes = pd.DataFrame(
                        {'onPrem': on_prem_crimes.groupby(["Block", "Primary_Type", "Year"]).size()}).reset_index()
                    merged2 = pd.merge(blocks_3_crimes, on_prem_crimes, on=['Primary_Type', 'Year'])
                    rest_main_df = pd.DataFrame(temp_rest_data).transpose()
                    final_loop_merge = pd.merge(rest_main_df, merged2, on=['Block'])
                    final_frame = final_frame.append(final_loop_merge)

    final_frame = final_frame[['Year','categories','name','address','has_Tobacco_license','has_liqour_license','Primary_Type',
                               'total','ArrestCount','onPrem']]
    final_frame = final_frame.sort_values(["Year", 'total'], ascending=[True, False])

    final_frame = final_frame.rename(columns={'categories':'Business Type','name':'Business Name','has_Tobacco_license':'Has Tobacco License',
                                              'has_liqour_license':'Has Liquor License','Primary_Type':'Crime Type',
                                              'total':'#Crimes','ArrestCount':'#Arrests','onPrem':'#On Premises'})


    final_frame['Business Type'] = final_frame['Business Type'].apply(lambda x: refine_type(x))

    final_frame.to_csv('Results/crimes_report_3_blocks.csv', encoding='utf-8', index=False)

    print("Crime report is Generated with the name crimes_report_3_blocks.csv in the Results folder")


def refine_type(x):
    out = "Restaurant"
    if "grocery" in x.lower():
        out = "Grocery"
    elif "school" in x.lower():
        out = "School"
    elif "restaurant" in x.lower():
        out = "Restaurant"
    return out




generate_crime_reports_blocks()