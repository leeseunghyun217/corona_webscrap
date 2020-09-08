import smtplib 
import os
from requests_html import HTML, HTMLSession
from email.message import EmailMessage
import time 


session = HTMLSession()
r = session.get('https://search.naver.com/search.naver?sm=top_sug.pre&fbm=1&acr=2&acq=%EC%BD%94%EB%A1%9C&qdt=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%9819')

info_blocks = r.html.find('div.status_info',first=True)
info_block = info_blocks.find('li')

lst = []

for info in info_block:
    total_num = info.find('p',first=True).text
    daily_num = info.find('em',first=True).text
    lst.append(total_num);lst.append(daily_num)

string =  'Total cases : {lst[0]} \
           Daily cases :{lst[1]} \
           Total testing : {lst[2]} \
           Daily testing : {lst[3]} \
           Total recovered : {lst[4]} \
           Daily recovered: {lst[5]} \
           Total deaths : {lst[6]} \
           Daily deaths : {lst[7]} '
    
EMAIL_ADD = os.environ.get('EMAIL_ID')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Corona Alert!' # enter subject of mail 
msg['From'] = EMAIL_ADD # enter sender email
msg['To'] = EMAIL_ADD # enter receiver email 

# Sending mail to multiple users 
#---------------------------------------------------
# contacts = ['user1@mail.com','user2@mail.com'...]

# Method 1 : 
# msg['To'] = contacts 

# Method 2 ( Method 1 sometimes does not work / msg['To'] reads comma seperated strings ) : 
# msg['To'] = ','.join(contacts) 

msg.set_content(string) # text if html is not read by email 

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

total_cases = lst[0]

def check_data(): # check if total cases changed 
    if lst[0] != total_cases:
        send_mail()

def send_mail():
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADD,EMAIL_PASS)
        smtp.send_message(msg)

while True:  
    check_data()
    time.sleep(42000) # set time ( seconds ) to time desired. 


