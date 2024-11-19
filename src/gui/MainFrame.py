# MainFrame.py
# HSVBoundaries
# 18/nov/2024
# cenfra




__version__ = "0.1"




import wx
import os
import json
from ..utils.dip import dip
from src.gui.PanelBoundaryValue import PanelBoundaryValue
from src.gui.PanelPreviewSource import PanelPreviewSource
from src.gui.FrameEditBoundary import FrameEditBoundary
import wx.adv




class MainFrame(wx.Frame):
    
    def __init__(self, parent, config, *args, **kwargs):

        # initialize the frame
        super().__init__(parent, *args, **kwargs)

        self.SetTitle("HSV Boundaries Tool")
        self.SetClientSize(dip(780, 450))

        # create initial config, which will be used to share the
        # program data between classes
        self.config = config

        self._init_ui()



        
    def _init_ui(self):

        self._init_menubar()

        # ----------------------- main panel ----------------------- #

        # the main panel will hold two panels, the panel where the
        # current boundaries are displayed and the panel where the
        # source preview (image, video or webcam) is displayed.

        self.panelMain = wx.Panel(self)
        self.sizerMain = wx.GridBagSizer()
        self.panelMain.SetSizer(self.sizerMain)

        # ---------------- boundaries panel (left) ---------------- #

        # this panel, along with the scrolled window inside it, will
        # hold the info panels for the currently set hsv boundaries.

        # create boundaries panel and sizer
        self.panelBoundaries = wx.Panel(self.panelMain)
        self.panelBoundaries.SetMinSize(dip(300, -1))
        self.panelBoundaries.SetMaxSize(dip(300, -1))
        self.panelBoundaries.SetBackgroundColour(wx.WHITE)
        self.sizerBoundaries = wx.BoxSizer(wx.VERTICAL)
        self.panelBoundaries.SetSizer(self.sizerBoundaries)
        
        # create scrolled window for boundaries and its sizer
        self.scrolledBoundaries = wx.ScrolledWindow(self.panelBoundaries)
        self.sizerScrolledBoundaries = wx.BoxSizer(wx.VERTICAL)
        self.scrolledBoundaries.SetSizer(self.sizerScrolledBoundaries)

        # set the scrolledwindow scrollbars
        self.scrolledBoundaries.SetScrollbars(20, 20, 55, 40)

        # add scrolled window to boundaries panel and update layout
        self.sizerBoundaries.Add(self.scrolledBoundaries, proportion=1, flag=wx.EXPAND)
        self.sizerBoundaries.Layout()

        # ------------------ source panel (right) ------------------ #

        # the source panel holds the panel that displays the
        # image/video/webcam preview.

        # create source panel and sizer
        self.panelSource = wx.Panel(self.panelMain)
        self.panelSource.SetBackgroundColour(wx.LIGHT_GREY)
        self.sizerSource = wx.BoxSizer(wx.VERTICAL)
        self.panelSource.SetSizer(self.sizerSource)

        self.panelPreview = PanelPreviewSource(parent=self.panelSource, config=self.config, inEditMode=False)

        self.sizerSource.Add(self.panelPreview, proportion=1, flag=wx.EXPAND|wx.ALL, border=dip(10))

        # ------------------ add panels to sizer ------------------ #

        # here we add the panels to the main panel's sizer

        self.sizerMain.Add(self.panelBoundaries, pos=(0, 0), flag=wx.EXPAND)
        self.sizerMain.Add(self.panelSource, pos=(0, 1), flag=wx.EXPAND)

        self.sizerMain.AddGrowableCol(1, 1)
        self.sizerMain.AddGrowableRow(0, 1)
        
        self.sizerMain.Layout()

        


    def _init_menubar(self):
        
        """Initializes the frame's menubar."""
        
        self.menubar = wx.MenuBar()

        # ----------------------- file menu ----------------------- #

        fileMenu = wx.Menu()
        fileMenu.Append(101, "Open JSON...", "")
        fileMenu.Append(102, "Save JSON...", "")
        fileMenu.AppendSeparator()
        fileMenu.Append(103, "Exit", "")

        self.Bind(wx.EVT_MENU, self._menubar_on_open, id=101)
        self.Bind(wx.EVT_MENU, self._menubar_on_save, id=102)
        self.Bind(wx.EVT_MENU, lambda event: self.Destroy(), id=103)

        # -------------------- boundaries menu -------------------- #
        
        boundariesMenu = wx.Menu()
        boundariesMenu.Append(201, "Add lower and upper boundary...", "")

        self.Bind(wx.EVT_MENU, self._menubar_on_add_boundary, id=201)

        # ---------------------- source menu ---------------------- #

        sourceMenu = wx.Menu()
        sourceMenu.Append(301, "Set video or image source...", "")
        sourceMenu.Append(302, "Set camera source...", "")

        self.Bind(wx.EVT_MENU, self._menubar_on_set_source_path, id=301)
        self.Bind(wx.EVT_MENU, self._menubar_on_set_source_camera, id=302)

        # ----------------------- help menu ----------------------- #

        helpMenu = wx.Menu()
        helpMenu.Append(401, "About...", "")

        self.Bind(wx.EVT_MENU, self._menubar_on_about, id=401)

        # ---------------------- append menus ---------------------- #

        self.menubar.Append(fileMenu, "File")
        self.menubar.Append(boundariesMenu, "Boundaries")
        self.menubar.Append(sourceMenu, "Source")
        self.menubar.Append(helpMenu, "Help")

        self.SetMenuBar(self.menubar)


        

    def _menubar_on_open(self, event):
        
        """Opens a file dialog and reads the JSON data into the config
        hsvBounds dictionary."""

        with wx.FileDialog(self, "Open JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding="utf-8") as file:
                    data = json.load(file)
            except:
                return

            self.config.hsvBounds = data
            self.config.activeBounds = [key for key in data.keys()]
            self.config.jsonPath = pathname

            # refresh the boundaries panel with the new hsvBounds
            self._refresh_boundaries_panels() 



            
    def _menubar_on_save(self, event):
        
        """Opens a file dialog and saves the hsvBounds data into a JSON file."""

        # if the user opened an existing JSON file, we will set its
        # name as the default save file name. 
        jsonPathFileName = os.path.basename(self.config.jsonPath)

        with wx.FileDialog(self, "Save JSON file", wildcard="JSON files (*.JSON)|*.JSON",
                           style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, defaultFile=jsonPathFileName) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding="utf-8") as file:
                    json.dump(self.config.hsvBounds, file)
                    self.config.jsonPath = pathname
            except:
                wx.MessageDialog(self, "Error saving JSON.", caption="Error",
                                 style=wx.OK|wx.CENTRE).ShowModal()



                
    def _menubar_on_set_source_path(self, event):
        
        """Opens file dialog and sets the path for the image/video source."""
        
        wildcard = (
            "Image and Video files (*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.mp4;*.avi;*.mov;*.mkv)|"
            "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.mp4;*.avi;*.mov;*.mkv|"
            "All files (*.*)|*.*"
        )

        with wx.FileDialog(self, message="Open Image/Video File", wildcard=wildcard,
                           style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            self.config.sourcePath = fileDialog.GetPath()
            self.panelPreview.SetSource(self.config.sourcePath)




    def _menubar_on_set_source_camera(self, event):
        
        """Opens a text dialog where the user specifies the camera as an int."""

        dlg = wx.TextEntryDialog(self, message="Enter camera number (int):", caption="Camera Number", value="0")

        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        value = dlg.GetValue()

        if not value.isdigit():
            wx.MessageDialog(self, message="The camera must be an integer (opencv).", caption="Error setting camera",
                             style=wx.OK|wx.CENTRE).ShowModal()
            return
        
        self.config.sourcePath = int(dlg.GetValue())
        self.panelPreview.SetSource(self.config.sourcePath)
        


            
    def _menubar_on_add_boundary(self, event):

        # if the source is a camera, we need to release it so that the
        # FrameEditBoundary (which has another preview panel) can open
        # the camera too. the FrameEditBoundary frame will resume our
        # preview once it is done.
        if type(self.panelPreview.source) == int:
            self.panelPreview.pause()
            
        frame = FrameEditBoundary(self, self.config, boundaryName="", mode="add", mainFrame=self)
        frame.Show()




    def _menubar_on_about(self, event):

        """Opens about dialog."""
        
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("HSV Boundary Tool")
        aboutInfo.SetVersion(__version__)
        aboutInfo.SetDescription(("Tool for determining HSV boundaries."))
        aboutInfo.AddDeveloper("cenfra")
        wx.adv.AboutBox(aboutInfo)



        
    def _refresh_boundaries_panels(self):

        """Destroys and re-displays the info panels for the existing boundaries."""
        
        # delete existing boundary panels
        for item in self.sizerScrolledBoundaries.GetChildren():
            window = item.GetWindow()
            if window:
                self.sizerScrolledBoundaries.Detach(window)
                window.Destroy()
        # display panels
        for item in self.config.hsvBounds:
            window = PanelBoundaryValue(parent=self.scrolledBoundaries, boundaryName=item, config=self.config, mainFrame=self)
            self.sizerScrolledBoundaries.Add(window, 0, wx.EXPAND|wx.ALL, border=dip(5))
        self.sizerScrolledBoundaries.Layout()
        self.sizerBoundaries.Layout()
        
