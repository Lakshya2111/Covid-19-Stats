from bs4 import BeautifulSoup
import requests, smtplib, csv
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from prettytable import PrettyTable
import time
def send_mail(table1,table2,text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    user='lakshyaj21@gmail.com'
    password='ojxgtqdlqelobpox'
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Covid-19 Statistics'
    message['From'] = user
    message['To'] = user
    html="""
        <html>
            <body>
                <p style="font-size:18px">Countries with most cases:</p>
                {}
                <br>
                <p style="font-size:18px">Data for India:<p>
                {}
                <br>
                <p style="font-size:14px">Check https://www.worldometers.info/coronavirus/ for more information.</p>
            </body>
        </html>
        """.format(table1,table2)
    part1=MIMEText(text,'plain')
    part2=MIMEText(html,'html')
    message.attach(part1)
    message.attach(part2)
    server.login(user,password)
    server.sendmail(user,user,message.as_string())
    server.quit()

while(True):
    URL=requests.get('https://www.worldometers.info/coronavirus/').text
    soup=BeautifulSoup(URL,'lxml')

    table=soup.find(id='main_table_countries_today')
    data=[]
    for i in table.find_all('th'):
        data.append(i.text)
    data[0]="S.No."
    data=data[:10]
    message=""
    for i in range(1,len(data)):
        for j in range(1,len(data[i])):
            if data[i][j]==",":
                data[i]=data[i][:j]
                break
            if data[i][j].isupper():
                data[i]=data[i][:j]+" "+data[i][j:]
                break
    count_row=0
    stats=[data]
    world =  soup.find('td', string='World').parent
    world_data=[]
    for k in world.find_all('td', limit=10):
        world_data.append(k.text)
    stats.append(world_data)
    for index in ['1','2','3']:
        parent=soup.find('td', string=index).parent
        temp=[]
        for i in parent.find_all('td', limit=10):
            temp.append(i.text)
        stats.append(temp)
    message+="Countries with most cases: \n\n"
    stats[1][0]='#'
    for stat in stats:  
        for j in stat:
            if j=="":
                hyp="-"
                message+=hyp.ljust(16)
                continue
            message+=j.ljust(16)
        message+="\n\n"
    message+="Data for India: \n\n"
    my_country=soup.find('td', string='India').parent
    my_country_data=[]
    my_country_data_table=[]
    for i in my_country.find_all('td',limit=10):
        my_country_data.append(i.text)
    for i in range(1,len(my_country_data)):
        my_country_data_table.append([stats[0][i],my_country_data[i]])
        message+=stats[0][i].ljust(16)
        message+=": "
        message+=my_country_data[i]+"\n"
    message+="\n\n"
    message+="Check https://www.worldometers.info/coronavirus/ for more information."

    for i in range(len(stats)):
        for j in range(len(stats[i])):
            if stats[i][j]=="":
                stats[i][j]="NA"

    table1=PrettyTable(stats[0])
    for i in range(1,len(stats)):
        table1.add_row(stats[i])
    table1=table1.get_html_string()
    table=open('table1.html','w')
    table.write(table1)

    table2=PrettyTable(my_country_data_table[0])
    for i in range(1,len(my_country_data_table)):
        table2.add_row(my_country_data_table[i])
    table2=table2.get_html_string()

    print(message)
    send_mail(table1,table2,message)
    time.sleep(86400)