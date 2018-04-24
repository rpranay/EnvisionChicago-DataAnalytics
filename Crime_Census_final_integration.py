import pandas as pd


df1=pd.read_csv("Crimes_Data_query_9.csv",nrows=300000)
df2=pd.read_csv("Cleaned_Census.csv")
df3=pd.DataFrame()
block=[]
ptype=[]
year=[]
tracts=[]
arrest=[]
for i in df1.index:
    print(i)
    lat=df1.iloc[i,4]
    lon=df1.iloc[i,5]
    max_lat=lat+0.001
    max_lon=lon+0.001
    min_lat=lat-0.001
    min_lon=lon-0.001
    temp_df=df2[(df2['lattitude'] >= min_lat) & (df2['lattitude'] <= max_lat) & (
                        df2['longitude'] <= min_lon) & (df2['longitude'] <= max_lon)]
    if(temp_df.size>0):
        block.append(df1.iloc[i, 1])
        ptype.append(df1.iloc[i, 2])
        year.append(df1.iloc[i, 3])
        arrest.append(df1.iloc[i,6])
        tracts.append(temp_df.iloc[0,1])

df3['block']=block
df3['ptype']=ptype
df3['year']=year
df3['Arrest']=arrest
df3['tract_block']=tracts
df3.to_csv("Crime_Census_Integrated.csv")

