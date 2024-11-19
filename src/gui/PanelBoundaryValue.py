# PanelBoundaryValue.py
# HSVBoundaries
# 18/nov/2024
# cenfra




import wx
from ..utils.dip import dip
from .FrameEditBoundary import FrameEditBoundary




class PanelBoundaryValue(wx.Panel):

    """This panel holds the checkbox (representing if the mask for the
    boundary is active or not), the name and the edit/remove buttons
    representing a boundary pair.
    """
    
    def __init__(self, parent, boundaryName, config, mainFrame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.boundaryName = boundaryName
        self.config = config
        self.mainFrame = mainFrame

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # ---------------------- set up sizer ---------------------- #

        self.sizer = wx.GridBagSizer()
        self.SetSizer(self.sizer)

        # ---------- create boundary checkbox and buttons ---------- #

        self._checkbox = wx.CheckBox(self, label=self.boundaryName)
        self._checkbox.SetValue(1)

        panelButtons = wx.Panel(self)
        sizerButtons = wx.BoxSizer()
        panelButtons.SetSizer(sizerButtons)
        self._buttonEdit = wx.Button(panelButtons, label="Edit...", size=dip(-1, 30))
        self._buttonRemove = wx.Button(panelButtons, label="Remove", size=dip(-1, 30))
        sizerButtons.Add(self._buttonEdit, 1, flag=wx.LEFT, border=dip(5))
        sizerButtons.Add(self._buttonRemove, 1, flag=wx.LEFT, border=dip(5))
        sizerButtons.Layout()

        self._checkbox.Bind(wx.EVT_CHECKBOX, self._on_checkbox)
        self._buttonEdit.Bind(wx.EVT_BUTTON, self._on_button_edit)
        self._buttonRemove.Bind(wx.EVT_BUTTON, self._on_button_remove)

        # ---------------------- add to sizer ---------------------- #

        self.sizer.Add(self._checkbox, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=dip(13))
        self.sizer.Add(panelButtons, pos=(0, 1), flag=wx.ALIGN_RIGHT|wx.ALL, border=dip(13))

        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableRow(0, 0)

        self.sizer.Layout()

        # ---------------------- bind events ---------------------- #

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_SIZE, self._on_size)


        

    def _on_paint(self, event):

        # get drawing contexts
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()

        gcdc.Clear()

        rect:wx.Rect = self.GetClientRect()
        rect = rect.Deflate(dip(2, 2))
        
        gcdc.SetPen(wx.Pen(wx.Colour(200, 200, 200), width=1))
        gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
        gcdc.DrawRoundedRectangle(rect, radius=dip(5))



        
    def _on_size(self, event):

        """Refresh and update layout when the window is resized."""
        
        self.Refresh()
        self.Layout()
        self.sizer.Layout()


        

    def _on_checkbox(self, event):

        """Sets or unsets the boundary mask in the activeBounds so
        that it is drawn or not, depending on the checkbox state."""
        
        if self._checkbox.GetValue() and self.boundaryName not in self.config.activeBounds:
            self.config.activeBounds.append(self.boundaryName)
        elif not self._checkbox.GetValue() and self.boundaryName in self.config.activeBounds:
            self.config.activeBounds.remove(self.boundaryName)


            

    def _on_button_edit(self, event):

        """Opens a frame to edit the boundary values."""
        
        frame = FrameEditBoundary(self, config=self.config, boundaryName=self.boundaryName,
                                  mode="edit", mainFrame=self.mainFrame)
        frame.Show()



        
    def _on_button_remove(self, event):

        """Deletes the boundary and refreshes panels."""
        
        del self.config.hsvBounds[self.boundaryName]
        self.mainFrame._refresh_boundaries_panels()
