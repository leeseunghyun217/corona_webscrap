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


EMAIL_ADD = os.environ.get('EMAIL_ID')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

string =  '총 확진자 : {lst[0]}명 \
            오늘 확진자 :{lst[1]}명\
            총 검사진행 : {lst[2]}명\
            오늘 검사진행 : {lst[3]}명\
            총 격리해제 : {lst[4]}명\
            오늘 격리해제 : {lst[5]}명\
            총 사망자 : {lst[6]}명\
            오늘 사망자 : {lst[7]}명'

msg = EmailMessage()
msg['Subject'] = '코로나 알람!'
msg['From'] = EMAIL_ADD
msg['To'] = EMAIL_ADD
msg.set_content(string)



msg.add_alternative('''\
<!doctype html>
<html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Corona Virus Numbers</title>
<body>
    <p>총 확진자 : {lst[0]}명</p>
    <p>오늘 확진자 :{lst[1]}명</p>
    <p>총 검사진행 : {lst[2]}명</p>
    <p오늘 검사진행 : {lst[3]}명</p>

    <p>총 격리해제 : {lst[4]}명</p>
    <p>오늘 격리해제 : {lst[5]}명</P>
    <p>총 사망자 : {lst[6]}명</p>
    <p>오늘 사망자 : {lst[7]}명</p>

</body>

    '''.format(**locals()),subtype = 'html')


total_cases = lst[0]

def check_data():
    if lst[0] != total_cases:
        send_mail()

def send_mail():
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADD,EMAIL_PASS)

        smtp.send_message(msg)

while True:  
    check_data()
    time.sleep(42000)


