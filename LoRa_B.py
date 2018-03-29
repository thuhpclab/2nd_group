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
#url_A='https://api.thingspeak.com/channels/241665/feeds/last.xml?timezone=Asia/Taipei'
url_B='https://api.thingspeak.com/channels/256131/feeds/last.xml?timezone=Asia/Taipei'
#url_C='https://api.thingspeak.com/channels/306218/feeds/last.xml?timezone=Asia/Taipei'
#url_D='https://api.thingspeak.com/channels/330089/feeds/last.xml?timezone=Asia/Taipei'
html=requests.get(url_B)
html.encoding='utf-8'
sp=BeautifulSoup(html.text,'html.parser')
tab_66=sp.find("feed")
time=tab_66.find("created-at").string
time=time.strip("+08:00")
time=time.replace("T"," ")

date=time.replace("-","/")
nid=tab_66.find("entry-id").string
hum=tab_66.find("field1").string
temp=tab_66.find("field2").string
PM25=tab_66.find("field3").string
PM10=tab_66.find("field4").string

cursor.execute("SET NAMES UTF8")
select_sql="select * from LoRa where `timestamp`= %s and `sensor`='B'"
cursor.execute(select_sql,date)
result=cursor.fetchall()
conn.commit()
b = 'B'
if result==():
	insert_sql="insert into LoRa values('{}',{},{},{},{},'{}','{}')".format(b,temp,hum,PM25,PM10,date,nid)
	cursor.execute(insert_sql)
	conn.commit()
else:
	conn.close()
#print(date)

