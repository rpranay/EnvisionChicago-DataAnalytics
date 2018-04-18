import pandas as pd
import numpy as np
import csv

df1=pd.read_csv("Business_Licenses.csv",nrows=300000)
df2=pd.read_csv("Cleaned_Census.csv")
df3=pd.DataFrame()
name=[]
address=[]
license_dec=[]
business_dec=[]
tract=[]
for i in df1.index:
    print(i)
    lat=df1.iloc[i,31]
    lon=df1.iloc[i,32]
    max_lat=lat+0.001
    max_lon=lon+0.001
    min_lat=lat-0.001
    min_lon=lon-0.001
    temp_df=df2[(df2['lattitude'] >= min_lat) & (df2['lattitude'] <= max_lat) & (
                        df2['longitude'] <= min_lon) & (df2['longitude'] <= max_lon)]
    if(temp_df.size>0):
        name.append(df1.iloc[i, 4])
        address.append(df1.iloc[i, 6])
        license_dec.append(df1.iloc[i, 15])
        business_dec.append(df1.iloc[i,17])
        tract.append(temp_df.iloc[0,1])

df3['name']=name
df3['address']=address
df3['license description']=license_dec
df3['business description']=business_dec
df3['tract_block']=tract

df=df3
df['business description'].replace('', np.nan, inplace=True)
df.dropna(subset=['business description'], inplace=True)
df.to_csv("BL_Census_intermediate.csv")

print("Intermediate file created - this file contains business licences which have proper business description, the rest are removed as description is the key t solve this query")

InputFile=open("BL_Census_intermediate.csv","r");
OutputFile=open("BL_Census_Final_output.csv","w")
input_reader=csv.reader(InputFile)
output_reader=csv.writer(OutputFile)
head=["rownumber","name","address","license desc","business desc","tract_block"]
output_reader.writerow(head)
count = 0
for line in input_reader:
    if(count>0):
        line[4].replace("(","")
        line[4].replace(")","")
        line[4].replace("/","")
        desc=line[4].split()
        desc_new=[]
        for x in desc:
            desc_new.append(x.lower())
        if 'liquor' in desc_new:
            output_reader.writerow(line)
    count=count+1


print("Final file is created which has business licenses with liquor")