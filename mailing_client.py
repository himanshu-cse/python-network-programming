import smtplib

import os
from dotenv import load_dotenv

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

load_dotenv()
email = os.getenv("EMAIL")
pswd = os.getenv("PASSWORD")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(email, pswd)

msg = MIMEMultipart()
msg['From'] = 'Himanshu Devatwal'
msg['To'] = 'devatwalhimanshu7@gmail.com'
msg['Subject'] = 'Just a text'

with open('mail_message.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

filename = 'mail_image.png'
attachment = open(filename, 'rb') # reading byte mode

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(p)

text = msg.as_string()
server.sendmail(email, 'devatwalhimanshu7@gmail.com', text)

server.quit()