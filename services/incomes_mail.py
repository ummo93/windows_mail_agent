# -*- coding: utf-8 -*-
import imaplib
import email
import os

# Создаём файл для записи сообщений(Название файла: текущее время)
file_name = 'LastMessage'
f_message = open('./tmp/'+file_name+".txt", 'w')

# Соединяемся с сервером через imap4_ssl
username = ""
password = ""
income_host = ""
income_port = ""

stream = open('settings.ini')
line = file.readline(stream)
try:
    while True:
        line = file.next(stream)
        if line.split('=')[0] == 'user_name':
            username = line.split('=')[1].strip()
        elif line.split('=')[0] == 'income_server':
            income_host = line.split('=')[1].strip()
        elif line.split('=')[0] == 'user_pass':
            password = line.split('=')[1].strip()
        elif line.split('=')[0] == 'income_port':
            income_port = line.split('=')[1].strip()
except StopIteration, stop:
    pass
finally:
    file.close(stream)

gmail = imaplib.IMAP4_SSL(income_host, income_port)
gmail.login(username, password)

# Выбирает из папки входящие непрочитанные сообщения
typ, count = gmail.select('INBOX')

# Выводит количество непрочитанных сообщений в папке входящие
typ, unseen = gmail.status('INBOX', "(UNSEEN)")
# print unseen

# Главный блок
typ, data = gmail.search(None, '(UNSEEN)')
for i in data[0].split():
    typ, message = gmail.fetch(i, '(RFC822)')

    # Открываем временный файл для записи и выводим письмо
    f_temp = open('temp', "w+")
    f_temp.write(message[0][1])

    # Закрываем временный файл
    f_temp.close()

    # Открываем временный файл для чтения
    f_temp = open('temp', "r")
    mail = email.message_from_file(f_temp)

    # Получаем дату письма и печаем в f_message - файл для записи сообщений
    msg_date = mail.get('Date')
    h = email.Header.decode_header(msg_date)
    msg_date = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]
    f_message.write("Date: " + msg_date)

    # Получаем отправителя письма и печаем в f_message - файл для записи сообщений
    sender = mail.get('From')
    h = email.Header.decode_header(sender)
    sender = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]
    temp = sender.encode('utf-8')
    f_message.write("\nSender: " + temp)

    # Получаем тему письма и печаем в f_message - файл для записи сообщений
    subject = mail.get('Subject')
    h = email.Header.decode_header(subject)
    subject = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]
    temp = subject.encode('utf-8')
    f_message.write("\nSubject: " + temp)

    # Закрываем временный файл
    f_temp.close()

# Закрываем файлы
f_message.close()

# Отключаемся от сервера gmail.com
gmail.close()
gmail.logout()
