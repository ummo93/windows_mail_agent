# coding=utf8
import sys
from services.mail import send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import wx

toaster = wx.App()

qtCreatorFile = './forms/main_window.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

server = ""
port = ""
username = ""
password = ""


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('./resources/gmail.ico'))

    @staticmethod
    def send_email(element_text):
        if len(recipient_input.text()) == 0:
            wx.NotificationMessage(u"Внимание!", u"Заполните email получателя!").Show()
        else:
            wx.NotificationMessage(u"Отправка Email", u"Начинаю отправку, это может занять до 1 минуты").Show()
            try:
                global server
                global port
                global username
                global password

                stream = open('settings.ini')
                line = file.readline(stream)
                server = line.split('=')[1]
                try:
                    while True:
                        line = file.next(stream)
                        if line.split('=')[0] == 'port':
                            port = line.split('=')[1]
                        elif line.split('=')[0] == 'user_name':
                            username = line.split('=')[1]
                        elif line.split('=')[0] == 'user_pass':
                            password = line.split('=')[1]
                except StopIteration, stop:
                    print "Чтение завершено"
                    send_email(recipient_input.text(), element_text.toPlainText(), server.strip(), port.strip(),
                               username.strip(), password.strip())
                    wx.NotificationMessage(u"Отправка Email", u"Сообщение успешно отправлено").Show()
                    element_text.clear()
                finally:
                    file.close(stream)
            except Exception, error:
                wx.NotificationMessage(u"Ошибка отправки Email", str(error)).Show()

    @staticmethod
    def open_incomes():
        wx.NotificationMessage(u"Входящие", u"Эта функция ещё не реализована!").Show()

if __name__ == "__main__":
    # Initial app
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('DesktopMail')
    window = MyApp()
    window.show()
    toaster.MainLoop()  # Main loop for notify service

    # Code
    recipient_input = window.findChildren(QtWidgets.QLineEdit, 'recipient')[0]
    push_button = window.findChildren(QtWidgets.QPushButton, 'pushButton')[0]
    income_Button = window.findChildren(QtWidgets.QPushButton, 'incomeButton')[0]
    text_area = window.findChildren(QtWidgets.QPlainTextEdit, 'plainTextEdit')[0]
    push_button.clicked.connect(lambda: window.send_email(text_area))
    income_Button.clicked.connect(lambda: window.open_incomes())

    # Чтобы при закрытии не закрывалась програма
    # QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # Exit loop
    sys.exit(app.exec_())

