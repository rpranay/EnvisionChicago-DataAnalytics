from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from builtins import range

saveFile=open('Data/WeatherData.csv','a+')
saveFile.write("Zip,Year,month,MeanTemperature,MaxTemperature,MinTemperature\n")

def Results(myurl,zip,year,month,day):
    str=zip+","+year+","+month+","+day+","
    uClient=uReq(myurl)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    table=page_soup.find("table", {"id":"historyTable"})
    count =0
    str=""
    str=zip+","+year+","+month+","
    for row in table.find_all("tr"):
        if count>1 and count<5:
            trcount=0
            for col in row.find_all("td"):
                if trcount==1:
                    span=col.find("span",{"class":"wx-value"})
                    if(span is None):
                        str=str+"-,"
                        print("abc")
                    else:
                        str=str+span.string+","
                        print(span.string)
                    trcount=trcount+1
                else:
                    trcount=trcount+1
            count=count+1
        else:
            count=count+1
    saveFile.write(str[:-1]+"\n")


for zip in range(60601,60608):
    for year in range(2010,2018):
        for month in range(1,13):
            myurl="https://www.wunderground.com/history/airport/KORD/"
            urlext=str(year)+"/"+str(month)+"/1/"
            myurl=myurl+urlext
            myurl=myurl+"MonthlyHistory.html?req_city=Chicago&req_state=IL&req_statename=Illinois&reqdb.zip="+str(zip)+"&reqdb.magic=1&reqdb.wmo=99999"
            Results(myurl,str(zip),str(year),str(month),"1")
