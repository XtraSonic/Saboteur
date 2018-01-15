import threading
import wx
import time
import socket


class testThread(threading.Thread):
    def __init__(self, parent):
        self.parent = parent
        threading.Thread.__init__(self)

    def run(self):
        self.value = 1
        while 1:
            print(self.value)
            time.sleep(1)


class testGUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Test", size=(500, 270))
        panel = wx.Panel(self, -1)

        self.buttonStart = wx.Button(panel, -1, label="Start thread", pos=(0, 0))
        self.buttonChange = wx.Button(panel, -1, label="Change var", pos=(0, 30))
        panel.Bind(wx.EVT_BUTTON, self.startThread, id=self.buttonStart.GetId())
        panel.Bind(wx.EVT_BUTTON, self.changeVar, id=self.buttonChange.GetId())

    def startThread(self, event):
        self.the_thread = testThread(self)
        self.the_thread.start()

    def changeVar(self, event):
        # DO SOMETHING HERE THAT CHANGES 'x' IN THREAD TO 2...
        print("start sleep")
        time.sleep(3)
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.connect(("192.168.0.213", 4315))
        # client_socket.recv(64).decode()

        print("end sleep")
        self.the_thread.value = 2


if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = testGUI()
    frame.Show(True)
    app.MainLoop()
