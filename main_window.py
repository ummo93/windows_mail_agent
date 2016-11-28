# coding=utf8
import sys
from services.mail import send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import wx

toaster = wx.PyApp()

qtCreatorFile = './forms/main_window.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

server = ""
port = ""
username = ""
password = ""


class MyApp(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
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
                               username.strip(), password.strip(), subject_input.text())
                    wx.NotificationMessage(u"Отправка Email", u"Сообщение успешно отправлено").Show()
                    element_text.clear()
                finally:
                    file.close(stream)
            except Exception, error:
                wx.NotificationMessage(u"Ошибка отправки Email", str(error)).Show()

if __name__ == "__main__":
    # Initial app
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('DesktopMail')
    window = MyApp()
    window.show()
    toaster.MainLoop()  # Main loop for notify service

    # Code
    recipient_input = window.findChild(QtWidgets.QLineEdit, 'recipient')
    push_button = window.findChild(QtWidgets.QPushButton, 'pushButton')
    text_area = window.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit')
    subject_input = window.findChild(QtWidgets.QLineEdit, 'subject')

    push_button.clicked.connect(lambda: window.send_email(text_area))

    # Чтобы при закрытии не закрывалась програма
    # QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # Exit loop
    sys.exit(app.exec_())

