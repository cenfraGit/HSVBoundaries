# config.py
# HSVBoundaries
# 18/nov/2024
# cenfra




class Config:
    
    """Holds the program's data configuration."""
    
    def __init__(self):
        self.hsvBounds = {}
        self.activeBounds = []
        self.hsvEditLower = (0, 0, 0)
        self.hsvEditUpper = (179, 255, 255)
        self.sourcePath = ""
        self.jsonPath = ""

