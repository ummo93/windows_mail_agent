# coding:utf8
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
import subprocess
import time
qtCreatorFile = './forms/settings.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

server = ""
port = ""
username = ""
password = ""


class Settings(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('./resources/gmail.ico'))

    @staticmethod
    def save(ser, por, us, pas):
        finish_stream = open('settings.ini', "w")
        finish_stream.write("server="+ser +
                            "\n"+"port="+por +
                            "\n" + "user_name=" + us +
                            "\n" + "user_pass=" + pas)
        finish_stream.close()
        subprocess.Popen("python ./main_window.py", shell=True)
        time.sleep(1)
        window.showMinimized()

if __name__ == "__main__":
    # Initial app
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('DesktopMail')
    window = Settings()
    window.show()

    # Code
    try:
        stream = open('settings.ini')
        line = file.readline(stream)
        server = line.split('=')[1].strip()
        try:
            while True:
                line = file.next(stream)
                if line.split('=')[0] == 'port':
                    port = line.split('=')[1].strip()
                elif line.split('=')[0] == 'user_name':
                    username = line.split('=')[1].strip()
                elif line.split('=')[0] == 'user_pass':
                    password = line.split('=')[1].strip()
        except StopIteration, stop:
            print "Чтение завершено"
        finally:
            file.close(stream)

    except IOError, error:
        stream = open('settings.ini', 'w')
        file.close(stream)
    except IndexError, error:
        pass

    host_input = window.findChild(QtWidgets.QLineEdit, 'host_line')
    port_input = window.findChild(QtWidgets.QLineEdit, 'port_line')
    pass_input = window.findChild(QtWidgets.QLineEdit, 'pass_line')
    username_input = window.findChild(QtWidgets.QLineEdit, 'username_line')

    host_input.setText(server)
    port_input.setText(port)
    pass_input.setText(password)
    username_input.setText(username)

    save_all = window.findChild(QtWidgets.QPushButton, 'save_all')
    save_all.clicked.connect(lambda: window.save(host_input.text(), port_input.text(),
                                                 username_input.text(), pass_input.text()))

    sys.exit(app.exec_())

