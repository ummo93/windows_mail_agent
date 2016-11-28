# coding:utf8
import wx
import os
import subprocess
import time
import threading
import signal

RESOURCES_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)) + "/resources/"
TRAY_TOOLTIP = 'Email notificator'
TRAY_ICON = RESOURCES_DIR + 'gmail.png'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_refresh)
        self.let = None  # for subprocess
        self.th = None  # interval thread

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Refresh', self.on_refresh)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    # def on_left_down(self, event):
    #     print 'Tray icon was left-clicked.'

    def on_refresh(self, event):
        if self.check_email() == 0:
            wx.NotificationMessage(u"Обновление почты",
                                   u"Новых сообщений нет...").Show()

    def on_exit(self, event):
        wx.NotificationMessage(u"Пожалуйста подождите!",
                               u"Все процессы будут корректно завершены в течение минуты...").Show()
        wx.CallAfter(self.Destroy)
        self.th.join()

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()

        self.th = threading.Timer(sec, func_wrapper)
        self.th.start()
        return self.th

    def check_email(self):
        try:
            self.let = subprocess.Popen("python ./services/incomes_mail.py", shell=True)
            time.sleep(3)
            check_file = open('./tmp/LastMessage.txt')
            length = len(check_file.read())
            check_file.close()
            if length > 0:
                wx.NotificationMessage(u"Входящее сообщение", u"Войдите в свою почту и проверьте последнее сообщение").Show()
                return 1
            else:
                check_file.close()
                os.remove(r'./tmp/LastMessage.txt')
                return 0
        except Exception, e:
            pass


def main():
    app = wx.App(redirect=True)
    taskbar = TaskBarIcon()
    taskbar.set_interval(lambda: taskbar.check_email(), 60)
    app.MainLoop()

if __name__ == '__main__':
    main()

