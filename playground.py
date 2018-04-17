import csv
import string
import pandas as pd
import numpy as np









"""

df1=pd.read_csv("data/CensusBlockTIGER2010.csv")
df2=pd.read_csv("Zip_Tract.csv")
df3=pd.read_csv("WeatherData.csv")
df4=df1.join(df2.set_index('TRACTCE10'), on='TRACTCE10')
df4.dropna(subset=['Zip'], inplace=True)
df3['Year'].astype(str)
df3['month'].astype(str)
df3['MeanTemperature'].astype(str)
df3['MaxTemperature'].astype(str)
merge = pd.merge(df4,df3,on=['Zip'])
df5=df4.merge(df3, left_on='Zip', right_on='Zip', how='outer')
print(df5.head(5))


"""
censusFile = open("data/CensusBlockTIGER2010.csv", "r");
crimesFile = open("data/Crimes.csv", "r")
outputFile = open("Crimes_Census_Final_output.csv", "w")
census_reader = csv.reader(censusFile)
crimes_reader = csv.reader(crimesFile)
output_reader = csv.writer(outputFile)
total_count = 0
main_count = 0
head = ["year", "Primary Type", "Address", "lat", "lon", "the_geom", "state", "county", "tract", "block", "geoid", "name",
        "tract_block"]
output_reader.writerow(head)
for crimes_line in crimes_reader:
    new_input = []
    if (main_count > 0):
        if (crimes_line[19] == "" or crimes_line[20] == ""):
            continue
        lat = float(crimes_line[19])
        lat = format(float(lat), '.3f')
        lon = float(crimes_line[20])
        lon = format(float(lon), '.3f')
        count = 0
        for line in census_reader:
            location_found = 0
            loc_fl = []
            if count != 0:
                loc = line[0][16:len(line[0]) - 3]
                loc = loc.replace(",", "")
                loc = loc.replace("(", "")
                loc = loc.replace(")", "")
                locs = loc.split()
                for ele in locs:
                    ele = float(ele)
                    ele = format(ele, '.3f')
                    loc_fl.append(ele)
            count = count + 1
            lat_all = loc_fl[1::2]
            lon_all = loc_fl[::2]
            for i in range(len(lat_all)):
                if (float(lat_all[i]) - float(lat) <= 0.002 or float(lat_all[i]) - float(lat) >= -0.002):
                    if (float(lon_all[i]) - float(lon) <= 0.002 or float(lon_all[i]) - float(lon) >= -0.002):
                        output = []
                        output.append(crimes_line[17])
                        output.append(crimes_line[5])
                        output.append(crimes_line[3])
                        output.append(crimes_line[19])
                        output.append(crimes_line[20])
                        location_found = 1
                        output = output + line
                        output_reader.writerow(output)
                        break
            if (location_found == 1):
                break
        if (location_found == 0):
            total_count = total_count + 1
    main_count = main_count + 1

print("Final file is created which has crimes data attached to its respective ccensus blocks")
