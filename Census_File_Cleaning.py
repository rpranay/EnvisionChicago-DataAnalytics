import pandas as pd


df1=pd.read_csv("CensusBlockTIGER2010.csv")
avg_lat=[]
avg_log=[]
tract_block=[]
count=0
for i in range(0,len(df1.index)):    
    line=df1.loc[i]
    loc_fl=[]
    loc=line[0][16:len(line[0])-3]
    loc=loc.replace(",","")
    loc=loc.replace("(","")
    loc=loc.replace(")","")
    locs=loc.split()
    for ele in locs:
        ele=float(ele)
        #ele=format(ele, '.3f')
        loc_fl.append(ele)
    lat_all=loc_fl[1::2]
    lon_all=loc_fl[::2]
    avg=0
    count=0
    for ele in lat_all:
        avg=avg+ele
        count=count+1
    avg_lat.append(avg/count)
    avg=0
    count=0
    for ele in lon_all:
        avg=avg+ele
        count=count+1
    avg_log.append(avg/count)

print(len(avg_lat))
print(len(avg_log))
print(df1.shape)
df1['lattitude']=avg_lat
df1['longitude']=avg_log
df1=df1[['tract_block','lattitude','longitude']]
df1.to_csv("Cleaned_Census.csv")
print(df1.head(5))
    
