# PanelPreviewSource.py
# HSVBoundaries
# 18/nov/2024
# cenfra




import wx
import cv2
import numpy as np
from copy import deepcopy
from ..utils.dip import dip




class PanelPreviewSource(wx.Panel):

    """This panel displays the source selected by the user. Can be a
    camera source or an image/video source."""
    
    def __init__(self, parent, config, inEditMode=False, *args, **kwargs):
        
        super().__init__(parent, *args, **kwargs)

        self.config = config
        self.inEditMode = inEditMode
        self.showMask = True
        self.source = None
        self.capture = None
        self.image = None
        self.timer = wx.Timer(self)

        # avaialble formats (haven't tested if all work)
        self.image_formats = (".png", ".jpg", ".jpeg", ".bmp")

        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # the panel will be refreshed every timer event.
        self.timer.Start(33)


        

    def SetSource(self, source):

        if str(source).strip() == "":
            return # do nothing

        if self.capture and self.capture.isOpened():
            self.capture.release()

        self.source = source

        # if webcam source
        if isinstance(source, int):
            self.capture = cv2.VideoCapture(source)
        # if path to video or image
        elif isinstance(source, str):

            # if image source
            if source.lower().endswith(self.image_formats):
                
                self.capture = None
                self.image = cv2.imread(source)
                if self.image is not None:
                   self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            # if video source
            else:
                self.capture = cv2.VideoCapture(source)


                
                
    def _on_paint(self, event):

        # get drawing contexts
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()

        gcdc.Clear()

        rect:wx.Rect = self.GetClientRect()

        # update frame
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                h, w = frame.shape[:2]
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.showMask:
                    frame = self._combine_color_masks(frame)
                image = wx.Image(w, h, frame.tobytes())
                bitmap = image.ConvertToBitmap()
                bitmap.SetSize(rect.GetSize())
                gcdc.DrawBitmap(bitmap, 0, 0)

            else: # if video and if reaches the end, loop
                if isinstance(self.source, str) and not self.source.lower().endswith(self.image_formats):
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        elif self.image is not None:
            frame = deepcopy(self.image)
            h, w = frame.shape[:2]
            if self.showMask:
                frame = self._combine_color_masks(frame)
            image = wx.Image(w, h, frame.tobytes())
            bitmap = image.ConvertToBitmap()
            bitmap.SetSize(rect.GetSize())
            gcdc.DrawBitmap(bitmap, 0, 0)



            
    def _on_timer(self, event):
        self.Refresh()



        
    def _combine_color_masks(self, frame_rgb):

        """Combines the masks into a single one, depending on the
        respective activeBounds values (the active masks)"""
        
        frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
        masks = []

        if self.inEditMode:
            mask = cv2.inRange(frame_hsv, self.config.hsvEditLower, self.config.hsvEditUpper)
            result = cv2.bitwise_and(frame_rgb, frame_rgb, mask=mask)
            return result

        # generate masks based on HSV bounds
        for color, bounds in self.config.hsvBounds.items():
            if color not in self.config.activeBounds:
                continue
            lower = np.array(bounds['lower'])
            upper = np.array(bounds['upper'])
            mask = cv2.inRange(frame_hsv, lower, upper)
            masks.append(mask)

        if len(masks) == 0:
            return frame_rgb

        # combine all masks into one
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = cv2.bitwise_or(combined_mask, mask)

        result = cv2.bitwise_and(frame_rgb, frame_rgb, mask=combined_mask)

        return result


    

    def pause(self):
        if self.timer.IsRunning():
            if self.capture and self.capture.isOpened():
                self.capture.release()
            self.timer.Stop()


            

    def resume(self):
        if not self.timer.IsRunning():
            if type(self.source) == int:
                self.capture = cv2.VideoCapture(self.source)
            self.timer.Start(33)

