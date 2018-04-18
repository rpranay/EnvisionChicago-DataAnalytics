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


generate_restaurant_biz_integrated()