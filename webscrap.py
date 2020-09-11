import smtplib 
import os
import requests
import requests_html
from requests_html import HTML, HTMLSession
from email.message import EmailMessage
import time
import datetime
        
def get_info():
    
    session = HTMLSession()
    r = session.get('https://search.naver.com/search.naver?sm=top_sug.pre&fbm=1&acr=2&acq=%EC%BD%94%EB%A1%9C&qdt=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%9819')

    info_blocks = r.html.find('div.status_info',first=True)
    info_block = info_blocks.find('li')

    lst = []

    for info in info_block:
        total_num = info.find('p',first=True).text
        daily_num = info.find('em',first=True).text
        lst.append(total_num);lst.append(daily_num)
    
    return lst

def send_mail(data):
        
    EMAIL_ADD = 'corona.number.korea@gmail.com'
    EMAIL_PASS = 'Sltmdgus217@'
        
    string =  'Total cases : {lst[0]} \
               Daily cases :{lst[1]} \
               Total testing : {lst[2]} \
               Daily testing : {lst[3]} \
               Total recovered : {lst[4]} \
               Daily recovered: {lst[5]} \
               Total deaths : {lst[6]} \
               Daily deaths : {lst[7]} '

    msg = EmailMessage()
    msg['Subject'] = 'Corona Alert!' # enter subject of mail 
    msg['From'] = 'corona.number.korea@gmail.com' # enter sender email
    msg['To'] = 'corona.number.korea@gmail.com' # enter receiver email 
    msg.set_content(string) # text if html is not read by email
    
    lst = data

    msg.add_alternative('''\
    <!doctype html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Corona Virus Numbers</title>
    </head>
    <body>
        <p>Total cases : {lst[0]}</p>
        <p>Daily cases : {lst[1]}</p>
        <p>Total testing : {lst[2]}</p>
        <pDaily testing : {lst[3]}</p>
        <p>Total recovered : {lst[4]}</p>
        <p>Daily recovered : {lst[5]}</P>
        <p>Total deaths : {lst[6]}</p>
        <p>Daily deaths : {lst[7]}</p>
    </body>
    </html>
        '''.format(**locals()),subtype = 'html')
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('corona.number.korea@gmail.com','Sltmdgus217@')
        smtp.send_message(msg)

original_data = get_info() # get list of data 

print('Initial Data : ',original_data[0])

while True:
    cur_data = get_info()
    if cur_data[0] != original_data[0]:
        send_mail(cur_data)
        print('New data at {}'.format(datetime.datetime.now()))
    else:
        print('No new data at {}'.format(datetime.datetime.now()))
    
    time.sleep(7200)
    
    
