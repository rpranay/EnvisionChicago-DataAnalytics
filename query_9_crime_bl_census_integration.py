import pandas as pd
import numpy as np

def run_crime_extraction_for_census():
    df1=pd.read_csv("Data/CensusBlockTIGER2010.csv")
    df1['tract_block'].replace('', np.nan, inplace=True)
    df1.dropna(subset=['tract_block'], inplace=True)
    df1=df1[['the_geom','GEOID10','NAME10','tract_block']]

    df4=df1.groupby(['tract_block'],as_index=False).count()

    df2=pd.read_csv("Data/BL_Census_Final_output.csv")
    df2['tract_block'].replace('', np.nan, inplace=True)
    df2.dropna(subset=['tract_block'], inplace=True)
    df2=df2[['name','address','license desc','business desc','tract_block']]

    df5=df2.groupby(['tract_block'],as_index=False).count()

    df3=pd.read_csv("Data/Crime_Census_Integrated.csv")
    df3['tract_block'].replace('', np.nan, inplace=True)
    df3.dropna(subset=['tract_block'], inplace=True)
    df3=df3[['Primary Type','Arrest','tract_block']]

    df6=df3.groupby(['tract_block'],as_index=False).count()

    df7=df3
    df7 = df7.drop(df7[df7.Arrest == 0].index)
    df8=df7.groupby(['tract_block'],as_index=False).count()

    q1_result = pd.merge(df4, df5,on=['tract_block'])

    q2_result=pd.merge(q1_result,df6,on=['tract_block'])

    final_result=pd.merge(q2_result,df8,on=['tract_block'])


    final_result=final_result[['tract_block','license desc','Arrest_x','Arrest_y']]
    final_result = final_result.rename(columns={'tract_block': 'Tract Number', 'license desc': 'No of restaurants with liquor sold','Arrest_x':'No of total Crimes','Arrest_y':'No of total arrests'})

    final_result.to_csv("Results/query_9_result.csv",index=False)

    print("Output for query 9 is generated in the results directory")