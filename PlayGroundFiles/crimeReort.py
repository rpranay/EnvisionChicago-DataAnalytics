import pandas as pd
import pandasql as ps
import numpy as np
import re

from difflib import SequenceMatcher

def similar(a, b):
    a = a.lower()
    b = b.lower()
    regex = "[^ a-zA-Z0-9]"

    a = re.sub(regex, "", a)
    b = re.sub(regex, "", b)
    return SequenceMatcher(None, a, b).ratio()

def address_refine(str1):
    ad = str1.split()
    s = ""
    try:
        for x in ["st", "dr", "ave", "pl", "pky", "blvd"]:
            if x in ad[2].lower().strip():
                for n in range(0, 3):
                    s += ad[n] + " "
            elif x in ad[3].lower().strip():
                for n in range(0, 4):
                    s += ad[n] + " "
    except IndexError:
        return str1

    return replacing(s)

def replacing(a):
    a = a.lower()
    a = a.replace('avenue', 'ave')
    a = a.replace('street', 'st')
    a = a.replace('boulevard', 'blvd')
    a = a.replace('parkway', 'pky')
    a = a.replace('place', 'pl')
    a = a.replace('drive', 'dr')
    a = a.replace('\'', '')
    a = a.replace('and', '&')
    a = a.replace('express', 'exp')
    a = a.replace('pizzeria', 'pizza')
    a = a.replace('academy', 'ady')
    a = a.replace('union station', 'usn')
    a = a.replace('cafe', 'cf')
    a = a.replace('  ', ' ')
    return a


data_path = "data/Crimes.csv"
biz_data_path = "data/Business_Licenses.csv"
rest_path = "data/restaurants_60601-60606.csv"


def fetch_biz_data():

    df = pd.read_csv(biz_data_path)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['LEGAL_NAME', 'DOING_BUSINESS_AS_NAME', 'ADDRESS', 'LICENSE_DESCRIPTION', 'ZIP_CODE']]
    df.ZIP_CODE = df.ZIP_CODE.astype(str)
    df = df[df.ZIP_CODE.str.match('6060[0-9]')]
    df['Block'] = df['ADDRESS'].apply(lambda x: address_to_block(x))
    return df


def generate_restaurant_biz_integrated():

    new_df = pd.DataFrame()
    biz_frame = fetch_biz_data()
    df = pd.read_csv(rest_path, nrows=5000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['name', 'address', 'categories']]
    df['address'] = df['address'].apply(lambda x: address_refine(x))
    df['Block'] = df['address'].apply(lambda x: address_to_block(x))
    df = df[df['categories'].str.lower().str.contains('restaurants|grocery|schools')]
    df['matched_address'] = ""
    df['matched_name'] = ""
    df['licence_description'] = ""
    regex = "[^ a-zA-Z0-9]"

    for row in df.index:
        x = df.at[row, 'address'].lower().split(" ")

        if len(x) > 3:

            tempFrame = biz_frame[biz_frame['ADDRESS'].str.lower().str.contains(x[0], na=False)]
            tempFrame = tempFrame[tempFrame['ADDRESS'].str.lower().str.contains(x[2], na=False)]
            name = df.at[row, 'name'][:3]
            name = name.lower()
            tempFrame = tempFrame[tempFrame['DOING_BUSINESS_AS_NAME'].str.lower().str.startswith(name, na=False)]
            tempFrame = pd.DataFrame({'total': tempFrame.groupby(
                ["ADDRESS", "DOING_BUSINESS_AS_NAME", "LICENSE_DESCRIPTION"]).size()}).reset_index()

            for t_rows in tempFrame.index:

                org_name = re.sub(regex, "", df.at[row, 'name'])
                temp_name = re.sub(regex, "", tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME'])
                measure = similar(org_name, temp_name)
                if measure >= 0.7:
                    df.at[row, "matched_name"] = tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME']
                    df.at[row, "matched_address"] = tempFrame.at[t_rows, 'ADDRESS']
                    df.at[row, "licence_description"] = tempFrame.at[t_rows, 'LICENSE_DESCRIPTION']
                    new_df = new_df.append(df.loc[[row]])

    new_df.to_csv('data/Restaurant_Biz_Match.csv', encoding='utf-8', index=False)
    print("File is Generated with the name Restaurant_Biz_Match.csv in the data folder")



def address_to_block(x):
    other = " ".join(x.split(" ")[1:]).strip()
    x = x.split(" ")[0].strip()
    lenX = len(x) - 2
    zeros = []
    for i in range(3-lenX):
        zeros.append('0')
    x = "".join(zeros + list(x)[0:lenX]) + "XX " + other
    return x.lower()


def main():
    df = pd.read_csv(biz_data_path, nrows=5000000)
    #print(df)
    #q1 = """SELECT 'LEGAL NAME', count('LEGAL NAME') FROM df group by 'LEGAL NAME' """
    #print(ps.sqldf(q1, locals()))
    #print(df)
    #df3 = pd.DataFrame(df)

    df.columns = [c.replace(' ', '_') for c in df.columns]
    df2 = df[['LEGAL_NAME','DOING_BUSINESS_AS_NAME','ADDRESS','LICENSE_DESCRIPTION','ZIP_CODE']]

    #df1 = df.groupby(['LEGAL_NAME','DOING_BUSINESS_AS_NAME','ADDRESS','LICENSE_DESCRIPTION','ZIP_CODE']).size().to_frame()
    #dfg = df.groupby('LEGAL NAME')
    #ddd = pd.DataFrame({'count': df2.groupby(["LEGAL_NAME", "DOING_BUSINESS_AS_NAME", 'ADDRESS','LICENSE_DESCRIPTION','ZIP_CODE']).size()}).reset_index()
    #print(ddd.applymap(str))
    ddd = df2
    ddd.ZIP_CODE = ddd.ZIP_CODE.astype(str)

    #cond = ddd['ZIP_CODE'].contains('6060[0-9]')
    #ddd1 = ddd[cond]
    org =ddd
    org = ddd[ddd.ZIP_CODE.str.match('6060[0-9]')]

    print(org[org['DOING_BUSINESS_AS_NAME'] == "DELMONICO"])

    org['Block'] = org['ADDRESS'].apply(lambda x: address_to_block(x))
    print(org)

    return org

    #print(df2.columns)


    #print(df['count'].groupby(level=0, group_keys=False))




def crimes():
    df = pd.read_csv(data_path, nrows=5000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    #biz = main()
    df2 = df[['Block','Primary_Type','Arrest','Date','Latitude','Longitude']]
    df2['Block'] = df2["Block"].apply(lambda x: l_fun(x))
    df2['Date'] = df2["Date"].apply(lambda x: x.split("/")[2].split(" ")[0])

    df2 = pd.DataFrame({'ArrestCount': df2.groupby(['Block','Primary_Type','Date','Arrest','Latitude','Longitude']).size()}).reset_index()
    df2.loc[df2['Arrest'] == False, 'ArrestCount'] = 0

    #df2 = df2.sort_values('count')
    print(df2)
    return df2
    merged = pd.merge(biz, df2, on=['Block'])
    print(merged)
    return merged

def l_fun(x):
    return x.lower()


def main2():
    matched = []
    went = []
    new_df = pd.DataFrame()

    biz_frame = main()
    print(biz_frame.shape)
    df = pd.read_csv(rest_path, nrows=5000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['name', 'address', 'categories']]
    df['address'] = df['address'].apply(lambda x: address_refine(x))
    df['Block'] = df['address'].apply(lambda x: address_to_block(x))
    df = df[df['categories'].str.lower().str.contains('restaurants|grocery|schools')]
    df['matched_address'] = ""
    df['matched_name'] = ""
    df['licence_description'] = ""
    print(df.columns)

    ff = 0
    gg = 0
    hh = 0
    regex = "[^ a-zA-Z0-9]"
    loopC=0
    for row in df.index:
        loopC = loopC + 1

        x = df.at[row,'address'].lower().split(" ")
        if len(x)>3:
            hh = hh+1

            tempFrame = biz_frame[biz_frame['ADDRESS'].str.lower().str.contains(x[0], na =False)]
            tempFrame = tempFrame[tempFrame['ADDRESS'].str.lower().str.contains(x[2], na =False)]
            name = df.at[row, 'name'][:3]
            name = name.lower()
            tempFrame = tempFrame[tempFrame['DOING_BUSINESS_AS_NAME'].str.lower().str.startswith(name, na =False)]
            # ddd = pd.DataFrame({'count': df2.groupby(["LEGAL_NAME", "DOING_BUSINESS_AS_NAME", 'ADDRESS','LICENSE_DESCRIPTION','ZIP_CODE']).size()}).reset_index()

            tempFrame = pd.DataFrame({'total': tempFrame.groupby(["ADDRESS","DOING_BUSINESS_AS_NAME","LICENSE_DESCRIPTION"]).size()}).reset_index()


            for t_rows in tempFrame.index:
                gg = gg+1
                org_name = re.sub(regex,"",df.at[row,'name'])
                temp_name = re.sub(regex,"",tempFrame.at[t_rows,'DOING_BUSINESS_AS_NAME'])
                measure = similar(org_name, temp_name)
                if measure >= 0.7:
                    df.at[row,"matched_name"] = tempFrame.at[t_rows,'DOING_BUSINESS_AS_NAME']
                    df.at[row, "matched_address"] = tempFrame.at[t_rows,'ADDRESS']
                    df.at[row, "licence_description"] = tempFrame.at[t_rows, 'LICENSE_DESCRIPTION']
                    new_df = new_df.append(df.loc[[row]])
                    ff =ff+ 1
                    #break

    print(new_df)
    new_df.to_csv('restaurantsExtract.csv', encoding='utf-8', index=False)
    crime_frame = crimes()

    #final_frame = pd.DataFrame(columns=['Year','Business_Type','Business_Name', 'Address', 'Has_Tobacco_License'
     #                                   ,'Has_Liquor_License','Crime_Type','#Crimes','#Arrests','#OnPremises'])
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
            maxLat = lat + 0.00004000
            minLat = lat - 0.00004000
            maxLong = long + 0.00000000004000
            minLong = long - 0.00000000004000
            #blocks_3_crimes = crime_frame[crime_frame['Block'] == temp_rest_data['Block']]
            blocks_3_crimes = crime_frame[(crime_frame['Latitude'] >= minLat) & (crime_frame['Latitude'] <= maxLat) & (crime_frame['Longitude'] <= minLong) & (crime_frame['Longitude'] <= maxLong)]
            if blocks_3_crimes.size > 0:
                blocks_3_crimes1 = pd.DataFrame({'total': blocks_3_crimes.groupby(["Primary_Type", "Date"]).size()}).reset_index()
                blocks_3_crimes = blocks_3_crimes.groupby(['Primary_Type', 'Date'], as_index=False)[["ArrestCount"]].sum()
                blocks_3_crimes = pd.merge(blocks_3_crimes, blocks_3_crimes1, on=['Primary_Type','Date'])
                on_prem_crimes = crime_frame[crime_frame['Block'] == temp_rest_data['Block']]

                if on_prem_crimes.size > 0:
                    on_prem_crimes = pd.DataFrame({'onPrem': on_prem_crimes.groupby(["Block", "Primary_Type", "Date"]).size()}).reset_index()
                    merged2 = pd.merge(blocks_3_crimes, on_prem_crimes, on=['Primary_Type','Date'])

                    rest_main_df = pd.DataFrame(temp_rest_data).transpose()
                    final_loop_merge = pd.merge(rest_main_df, merged2, on=['Block'])
                    final_frame = final_frame.append(final_loop_merge)

    final_frame.to_csv('test.csv', encoding='utf-8', index=False)


"""
        rest_series = row[1]
        name = rest_series['name']
        block = rest_series['Block']
        address = rest_series['matched_address']
        biz_type = rest_series['categories']
"""
        #crime_data = crime_frame[crime_frame['Block'] == block]





        #print(row)





        #merged = pd.merge(crime_frame, new_df, on=['Block','Block'])
        #print(merged)


            #t_rows[]



        #print("done!!!!")












#main()
#crimes()
generate_restaurant_biz_integrated()
#main2()
#print(address_refine("122 S Michigan street Chicago, IL 60603 Neighborhood: The Loop"))
regex = "[^ a-zA-Z0-9]"

a = re.sub(regex, "", "bacci pizza italy inc")
b = re.sub(regex, "", "bacci's pizzaeria")
print(similar(a,b))
