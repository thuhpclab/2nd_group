# -*- coding: utf-8 -*-
import urllib3
import MySQLdb as mysql
import os,time,requests,sys,datetime
reload(sys)#重要編碼
from threading import Timer
from datetime import date
from bs4 import *
urllib3.disable_warnings()
sys.setdefaultencoding('utf8')

conn=mysql.connect(host="140.128.101.210",user="hpc",passwd="hpc123",db="Environment",charset="utf8")
cursor=conn.cursor()
def is_integer(x):
    try:
        return float(x)
    except ValueError:
        return -404.0

url_Time='http://taqm.epb.taichung.gov.tw/TQAMNEWAQITABLE.ASPX'


url_Observation='http://taqm.epb.taichung.gov.tw/aqi/aqiCAR.ASPX'
html=requests.get(url_Observation)
html.encoding='utf-8'
sp=BeautifulSoup(html.text,'html.parser')

html2=requests.get(url_Time)
html2.encoding='utf-8'
sp2=BeautifulSoup(html2.text,'html.parser')
Year=sp2.find_all('span')[1].string[16:20]
Mon=sp2.find_all('span')[1].string[21:23]
Day=sp2.find_all('span')[1].string[24:26]
Hour=sp2.find_all('span')[1].string[28:30]

SiteName=sp.find_all('td')[3].string[0:5]
County=u'臺中市'
if (sp.find_all('td')[5].string) == '0':
    AQI = ''
else:
    AQI = sp.find_all('td')[5].string

Pollutant=sp.find_all('td')[6].string
Status=sp.find_all('td')[4].string

if (sp.find_all('td')[8].string) == '0.0':
    SO2 = ''
else:
    SO2 = sp.find_all('td')[8].string

if (sp.find_all('td')[10].string) == '0.00':
    CO = ''
else:
    CO = sp.find_all('td')[10].string

CO_8hr=""

if (sp.find_all('td')[12].string) == '0.0':
    O3 = ''
else:
    O3 = sp.find_all('td')[12].string

O3_8hr=""

if (sp.find_all('td')[14].string) == '0':
    PM10 = ''
else:
    PM10 = sp.find_all('td')[14].string

if (sp.find_all('td')[18].string) == '0':
    PM25 = ''
else:
    PM25 = sp.find_all('td')[18].string

if (sp.find_all('td')[16].string) == '0.0':
    NO2 = ''
else:
    NO2 = sp.find_all('td')[16].string
NOx=""
NO=""
WindSpeed=""
WindDirec=""

PublishTime=Year+"-"+Mon+"-"+Day+" "+Hour+":00"
PM10_AVG=""
PM25_AVG=""

#print(url_Observation)
#print SiteName,County,AQI,Pollutant,Status,SO2,CO,CO_8hr,O3,O3_8hr,PM10,PM25,NO2,NOx,NO,WindSpeed,WindDirec,PublishTime,PM10_AVG,PM25_AVG

cursor.execute("SET NAMES UTF8")
select_sql="select * from airquality where `PublishTime`= %s and `SiteName`= %s "
cursor.execute(select_sql,(PublishTime,SiteName,))
result=cursor.fetchall()
conn.commit()
SiteName = SiteName
if result==():
    insert_sql="insert into airquality(id,SiteName,County,AQI,Pollutant,Status,SO2,CO,CO_8hr,O3,O3_8hr,PM10,PM25,NO2,NOx,NO,WindSpeed,WindDirec,PublishTime,PM10_AVG,PM25_AVG) values (null, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data= SiteName,County,AQI,Pollutant,Status,SO2,CO,CO_8hr,O3,O3_8hr,PM10,PM25,NO2,NOx,NO,WindSpeed,WindDirec,PublishTime,PM10_AVG,PM25_AVG
    cursor.execute(insert_sql,data)
    conn.commit()
else:
    conn.close()
