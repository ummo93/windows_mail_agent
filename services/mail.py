# coding=utf8
import smtplib
from email.mime.text import MIMEText


def send_email(recipient, text, server, port, username, password, subject_text="Mail from mail agent!"):
    # отправитель
    me = username
    # получатель
    you = recipient
    # текст письма
    text = unicode(text)
    # заголовок письма
    subj = subject_text

    # SMTP-сервер
    server = server
    port = port
    user_name = username
    user_passwd = password

    # формирование сообщения
    msg = MIMEText(text, "html", "utf-8")
    msg['Subject'] = subj
    msg['From'] = me
    msg['To'] = you

    # отправка
    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user_name, user_passwd)
    s.sendmail(me, you, msg.as_string())
    s.quit()
