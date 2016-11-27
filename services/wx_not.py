# TODO background tray status
import sys
import wx
app = wx.App()


class TestTaskBarIcon(wx.TaskBarIcon):

    def __init__(self, title, text):
        wx.TaskBarIcon.__init__(self)
        # create a test icon
        bmp = wx.EmptyBitmap(16, 16)
        dc = wx.MemoryDC(bmp)
        dc.SetBrush(wx.RED_BRUSH)
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)

        testicon = wx.EmptyIcon()
        testicon.CopyFromBitmap(bmp)

        self.SetIcon(testicon)
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, lambda e: (self.RemoveIcon(), sys.exit()))

        wx.NotificationMessage(title, text).Show()

def balloon_tip(title, text):
    wx.NotificationMessage(title, text).Show()

if __name__ == "__main__":
    icon = TestTaskBarIcon("Hello", "Hello world")
    app.MainLoop()
