# main.py
# HSVBoundaries
# 18/nov/2024
# cenfra


import wx
import platform
from src.config import Config
from src.gui.MainFrame import MainFrame


if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


# create initial config used to share and modify data through classes
config = Config()


if __name__ == "__main__":
    app = wx.App()
    instance = MainFrame(None, config)
    instance.Show()
    app.MainLoop()
