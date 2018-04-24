import pandas as pd



import pandas as pd

"""
df1=pd.read_csv("data/Crimes.csv",nrows=1000000)
df1 = df1[['Block', 'Primary Type','Year', 'Latitude', 'Longitude','Arrest']]
df1.to_csv("cropped_census.csv")
df2=pd.read_csv("Cleaned_Census.csv")
df3=pd.DataFrame()
block=[]
ptype=[]
year=[]
tracts=[]
arrest=[]
for i in df1.index:
    lat=df1.iloc[i,3]
    lon=df1.iloc[i,4]
    max_lat=lat+0.001
    max_lon=lon+0.001
    min_lat=lat-0.001
    min_lon=lon-0.001
    temp_df=df2[(df2['lattitude'] >= min_lat) & (df2['lattitude'] <= max_lat) & (
                        df2['longitude'] <= min_lon) & (df2['longitude'] <= max_lon)]
    if(temp_df.size>0):
        block.append(df1.iloc[i, 0])
        ptype.append(df1.iloc[i, 1])
        year.append(df1.iloc[i, 2])
        arrest.append(df1.iloc[i,5])
        tracts.append(temp_df.iloc[0,1])

df3['Arrest']=arrest
df3['block']=block
df3['ptype']=ptype
df3['year']=year
df3['tracts']=tracts
df3.to_csv("temp_result.csv")
"""
"""
df1=pd.read_csv("data/Crimes.csv",nrows=2000)
df1 = df1[['Block', 'Primary Type','Year', 'Latitude', 'Longitude']]
df2=pd.read_csv("data/CensusBlockTIGER2010.csv")
print(df1.shape)
df1.dropna(subset=['Latitude'], inplace=True)
df1.dropna(subset=['Longitude'], inplace=True)
print(df1.shape)
tract=[]
block=[]
tract_block=[]
print(len(df1.index))
for i in range(0,len(df1.index)):
    lat=float(df1.iloc[i,3])
    lat=format(float(lat), '.3f')
    lon=float(df1.iloc[i,4])
    lon=format(float(lon), '.3f')
    count=0
    j=i
    for k in range(0,len(df2.index)):
        line=df2.loc[k]
        if(j==i):
            print(i)
            j=j+1
        location_found=0
        loc_fl=[]
        if count!=0:
            loc=line[0][16:len(line[0])-3]
            loc=loc.replace(",","")
            loc=loc.replace("(","")
            loc=loc.replace(")","")
            locs=loc.split()
            for ele in locs:
                ele=float(ele)
                ele=format(ele, '.3f')
                loc_fl.append(ele)
        count=count+1
        lat_all=loc_fl[1::2]
        lon_all=loc_fl[::2]
        for j in range(len(lat_all)):
            if ((float(lat_all[j]) - float(lat) <= 0.002 and float(lat_all[j]) - float(lat) >= 0) or (
                    float(lat_all[j]) - float(lat) <= 0 and float(lat_all[j]) - float(lat) >= -0.002)):
                if ((float(lon_all[j]) - float(lon) <= 0.002 and float(lon_all[j]) - float(lon) >= 0) or (
                        float(lon_all[j]) - float(lon) <= 0 and float(lon_all[j]) - float(lon) >= -0.002)):
                    tract.append(line[3])
                    block.append(line[4])
                    tract_block.append(line[7])
                    location_found=1
                    break
        if(location_found==1):
#            print(i)
            break
    if(location_found==0):
        print("not found",i)

df1['tract']=tract
df1['block']=block
df1['tract_block']=tract_block


df1.to_csv("Crimes_Census_Temp_output.csv")
print(df1.shape)
"""

"""
import pandas as pd
import numpy as np

df1=pd.read_csv("data/CensusBlockTIGER2010.csv")
#df1.columns = [c.lower().replace(' ', '_') for c in df1.columns]
df1 = df1.rename(columns={"TRACT_BLOC":"tract_block"})
df1['tract_block'].replace('', np.nan, inplace=True)
df1.dropna(subset=['tract_block'], inplace=True)
df1=df1[['the_geom','GEOID10','NAME10','tract_block']]

df4=df1.groupby(['tract_block'],as_index=False).count()

df2=pd.read_csv("BL_Census_Final_output.csv")
df2['tract_block'].replace('', np.nan, inplace=True)
df2.dropna(subset=['tract_block'], inplace=True)
df2=df2[['id','name','address','license desc','business desc','lat','lon','tract_block']]


df5=df2.groupby(['tract_block'],as_index=False).count()

df3=pd.read_csv("temp_result.csv")
df3['tract_block'].replace('', np.nan, inplace=True)
df3.dropna(subset=['tract_block'], inplace=True)
df3=df3[['block','ptype','Arrest','tract_block']]

df6=df3.groupby(['tract_block'],as_index=False).count()

df7=df3
df7 = df7.drop(df7[df7.Arrest == 0].index)
df8=df7.groupby(['tract_block'],as_index=False).count()


q1_result = pd.merge(df4, df5,on=['tract_block'])

q2_result=pd.merge(q1_result,df6,on='tract_block')

final_result=pd.merge(q2_result,df8,on=['tract_block'])

print(final_result.head(5))


final_result=final_result[['tract_block','Arrest_y']]
final_result['id_x'].replace(np.nan, 0, inplace=True)
final_result['id_y'].replace(np.nan, 0, inplace=True)
final_result['Arrest_y'].replace(np.nan, 0, inplace=True)
print(final_result.head(10))
final_result.to_csv("query_9_temp_result.csv")


print("Final result for query 9 is extracted")
"""
import pandas as pd
import numpy as np

df1=pd.read_csv("data/Zip_Tract.csv")
df2=pd.read_csv("data/CensusBlockTIGER2010.csv")
df3=pd.read_csv("data/WeatherData.csv")
print(df3)
df3 = df3.drop('Unnamed: 0', 1)
df3.to_csv("Data/WeatherData.csv",index=False)

#df3['Zip1'] = df3.index

df4 = pd.merge(df1, df2,on=['TRACTCE10'])
df4=df4[['TRACT_BLOC','Zip']]
print(df4.head(5))

df5 = pd.merge(df4, df3,on=['Zip'])
print(df5.head(5))
