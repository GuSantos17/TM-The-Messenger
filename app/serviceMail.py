from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from decouple import config

def recoveryPass(newpass, user, email):

    msg = MIMEMultipart()

    message = "Seu usuário é: " + str(user) + " e a sua nova senha é: " + str(newpass)
    passwd = config('PASS_EMAIL')
    msg['from'] = config('EMAIL_FROM')
    msg['to'] = str(email)
    msg['Subject'] = "The Messenger - Recuperação de Senha"
    
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(config('SMTP_CONFIG'))
    server.starttls()

    server.login(msg['from'], passwd)
    server.sendmail(msg['from'], msg['to'], msg.as_string())
    server.quit() 