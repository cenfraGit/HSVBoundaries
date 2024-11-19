# FrameEditBoundary.py
# HSVBoundaries
# 18/nov/2024
# cenfra




import wx
import cv2
import numpy as np
from wx.lib.embeddedimage import PyEmbeddedImage
from .PanelPreviewSource import PanelPreviewSource
from ..utils.dip import dip



# embedded image instead of png file (was going to remove but lost the file)
image_hue = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAB1cAAAC1CAIAAACMHeExAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7DAdpqmNwAACMNSURBVHhe7djT1nRdloXRkbbtzD9t'
    b'27Zt27Zt27Zt27ZtGzN3rV1txYovdmS+FUd10Gcb9/C02TPdC5PaX9v+UwdoO2DqQKkDtx0k'
    b'ddC2g6UOnjpE2yFTh2o7dOowqcO2HS51+NQR2o6YOlLbkVNHSR217Wipo7cdI3XM1LHajp06'
    b'TttxU8dL7dd2/NQJ2k6YOlHqxG0nSZ207WSpk6dO0XbK1KnaTp06Teq0badLnT51hrYzps7U'
    b'dubUWVJnbTtb6uxt50idM3WutnOnztN23tT5Uudvu0Dqgm0XSl04dZG2i6Yu1nbx1CVSl2y7'
    b'VOrSbZdJXTZ1ubbLp66QumLblVJXbrtK6qqpq7VdPXWNtmumrpW6dtt1Utdtu17q+qkbtN0w'
    b'daO2G6dukrpp281SN2+7ReqWqVu13Tp1m7bbpm6Xun3bHVJ3TN2p7c6pu7TdNXW31N3b7pG6'
    b'Z9u9UvdO3aftvqn7td0/9YDUA9selHpw20NSD009rO3hqUe0PTL1qNSj2x6TemzqcW2PTz2h'
    b'7YmpJ6We3PaU1FPbnpZ6euoZbc9MPavt2annpJ7b9rzU89tekHph6kVtL069pO2lqZelXt72'
    b'itQr216VenXqNW2vTb0u9fq2N6Te2Pam1JtTb2l7a+ptbW9PvSP1zrZ3pd7d9p7Ue1Pva3t/'
    b'6gNtH0x9KPXhto+kPtr2sdTHU59o+2TqU22fTn0m9dm2z6U+n/pC2xdTX2r7cuorqa+2fS31'
    b'9bZvpL6Z+lbbt1Pfaftu6nup77f9IPXDth+lfpz6SdtPUz9r+3nqF6lftv0q9eu236R+m/pd'
    b'2+9Tf0j9se1PqT+3/SX119Tf2v6e+kfbP1P/StX/7F+Vf1b+Ufl75W9tf638pfLnyp8qf6z8'
    b'oe33ld9Vflv5TeXXbb+q/LLyi8rPKz9r+2nlJ5UfV35U+WHlB23fr3yv8t3KdyrfbvtW5ZuV'
    b'b1S+Xvla5attX6l8ufKlyhcrX2j7fOVzlc9WPlP5dNunKp+sfKLy8crHKh9t+0jlw5UPVT5Y'
    b'+UDb+yvvq7y38p7Kuyvvantn5R2Vt1feVnlr21sqb668qfLGyhvaXl95XeW1lddUXl15Vdsr'
    b'K6+ovLzysspL215SeXHlRZUXVl7Q9vzK8yrPrTyn8uzKs9qeWXlG5emVp1We2vaUypMrT6o8'
    b'sfKEyuPbHld5bOUxlUdXHtX2yMojKg+vPKzy0LaHVB5ceVDlgZUHVO7fdr/KfSv3qdy7cq+2'
    b'e1buUbl75W6Vu1bu0nbnyp0qd6zcoXL7tttVblu5TeXWlVu13bJyi8rNKzer3LRyk7YbV25U'
    b'uWHlBpXrt12vct3KdSrXrlyrcs22a1SuXrla5aqVq7RduXKlyhUrV6hcvu1ylctWLlO5dOVS'
    b'lUu2XaJy8crFKhetXKTtwpULVS5YuUDl/JXztZ23cp7KuSvnqpyz7RyVs1fOVjlr5SxtZ66c'
    b'qXLGyhkqp6+cru20ldNUTl05VeWUbaeonLxysspJKyepnLjtRJUTVk5QOX5lv7bjVY5bOU7l'
    b'2JVjtR2zcozK0StHqxy1cpS2I1eOVDli5QiVw7cdrnLYymEqh64cqu2QlUNUDl45WOWglYO0'
    b'HbhyoMoBKweo7L9tfzU1u28u9xzvXu4p23O5e7anZs/Z7s2egz03ew72XOs52HOtN1O92enN'
    b'SPdCT3meC93zPLW553lu8xzmuc1zmOcqz2Geqzwnea7ynOTNHm/GuJd4ynAv8ZzhqcE9w3OD'
    b'pwD3Bs8Bnus7B3iu75zeub5zeje7uxjdzeLOuZ1a23M7t3YKbW/tHNqpsj20c2XnxM6V7Ymd'
    b'+jontvd1M66bZd3M6tzUKai9qXNQp5r2oPaaTimda9pTOnV0Tmnv6BTRuaM9opsF3czn3M4p'
    b'nL2dm+HcrGZP5tTLOZm9l1Ms5172WG6WcjOTcyPnTM6N3Azk9jpOadys45zGsY49jb2OYxp7'
    b'Hcc0znXcJ41zHf9rGucu7pPGuYtjGnsXxzT2LvY0jl2c07iXLk5R3KeLcxT36eIcxbGLPYpj'
    b'F3sUexd3i+JUxM0oTkXcJ4pzEccojkXsURyLOEdxnyLOUfyvRZxyuFnEKYf7FLHncCxiz2Ev'
    b'4pjDuYj75HAu4m45nFs45rC3cMxhb2HP4djCOYf7tHDO4T4tnEI4tHBbCPf5Xzef120hHN/W'
    b'/1MIpwr+/wzh3MIdQtg/0f8cwrmFYwjnFv7XEI5/5+bT+R9C2N/NzV9z89EcQzi3cAzh3MIx'
    b'hL2FYwjHz3IOYW9hD2Fv4eJDuflNbr6SYwh7C3sIewt7CHsLxxD2FvYQ9hb2EI4t3HwZF//F'
    b'zWexh3C9hWMOF4u4+TIufo2Lj+NiIHsj+wc5NbJncrGUPZZzL+dY9l4uJnPxoVz8KXs7ez7H'
    b'z7IXdDGivaOLKV38MntQF5s6ZrW/m4sfZ4/r2Nf+d46J7ZWdQztVdgztYms3f9CxuIvR7d3t'
    b'z+iY3l7fxZd0scE9w/03nTLcS9xjPJW4x3jxQ+1J7lWektyr3MM8vqqL3+rmw7r4sy52uqe6'
    b'13pKda/1YrDXXlgKTIEpMAWmwBSYAlNgCkyBKTAFpsAUeKccUmAKTIEp8P+2kAJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUeFVcCkyBx6hSYApMgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBR6eXwpMgSkwBabAFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCjzluhebAlNgCkyBd3p7KTAFpsAUeLmOFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYArf2UmAKTIEpMAWmwBSYAlNgCkyBKXD/'
    b'NynwFMKhhdtCSIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAewshBabAFJgCU2AKTIEpMAVeLzMFpsAUmAJT'
    b'YApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAq+iSoEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApM'
    b'gSkwBabAFJgCU2AKTIEpMAWmwBR4eH4pMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSnwlOte'
    b'bApMgSkwBd7p7aXAFJgCU+DlOlJgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCkyBKTAFpsAUmAJTYArc2kuBKTAFpsAUmAJTYApMgSkwBabA/d+kwFMIhxZuCyEF'
    b'psAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabA'
    b'FJgCU2AKTIEpMAWmwBSYAu8thBSYAlNgCkyBKTAFpsAUeL3MFJgCU2AKTIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsAUmAJTYAq8iioFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJT4OH5pcAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwFOue7EpMAWmwBR4p7eX'
    b'AlNgCkyBl+tIgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabA'
    b'FJgCU2AKTIEpcGsvBabAFJgCU2AKTIEpMAWmwBSYAvd/kwJPIRxauC2EFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAU'
    b'mAJTYAq8txBSYApMgSkwBabAFJgCU+D1MlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AK'
    b'TIEp8CqqFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIGH'
    b'55cCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJPue7FpsAUmAJT4J3eXgpMgSkwBV6uIwWm'
    b'wBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsCt'
    b'vRSYAlNgCkyBKTAFpsAUmAJTYArc/00KPIVwaOG2EFJgCkyBKTAFpsAUmAJTYApMgSkwBabA'
    b'FJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp8N5CSIEp'
    b'MAWmwBSYAlNgCkyB18tMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsCrqFJgCkyB'
    b'KTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFHp5fCkyBKTAFpsAU'
    b'mAJTYApMgSkwBabAFJgCU2AKPOW6F5sCU2AKTIF3enspMAWmwBR4uY4UmAJTYApMgSkwBabA'
    b'FJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCt/ZSYApMgSkwBabA'
    b'FJgCU2AKTIEpcP83KfAUwqGF20JIgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAU'
    b'mAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsB7CyEFpsAUmAJTYApMgSkw'
    b'BV4vMwWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCr6JKgSkwBabAFJgCU2AKTIEp'
    b'MAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFHh4fikwBabAFJgCU2AKTIEpMAWmwBSY'
    b'AlNgCkyBKfCU615sCkyBKTAF3untpcAUmAJT4OU6UmAKTIEpMAWmwBSYAlNgCkyBKTAFpsAU'
    b'mAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCtzaS4EpMAWmwBSYAlNgCkyBKTAFpsD9'
    b'36TAUwiHFm4LIQWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSY'
    b'AlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgC7y2EFJgCU2AKTIEpMAWmwBR4vcwUmAJTYApM'
    b'gSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCryKKgWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlPg4fmlwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAU657'
    b'sSkwBabAFHint5cCU2AKTIGX60iBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSY'
    b'AlNgCkyBKTAFpsAUmAJTYApMgSlway8FpsAUmAJTYApMgSkwBabAFJgC93+TAk8hHFq4LYQU'
    b'mAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgC'
    b'U2AKTIEpMAWmwBSYAlNgCry3EFJgCkyBKTAFpsAUmAJT4PUyU2AKTIEpMAWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJTYApMgSnwKqoUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYApMgYfnlwJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAk+57sWmwBSYAlPgnd5e'
    b'CkyBKTAFXq4jBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgC'
    b'U2AKTIEpMAWmwK29FJgCU2AKTIEpMAWmwBSYAlNgCtz/TQo8hXBo4bYQUmAKTIEpMAWmwBSY'
    b'AlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJT'
    b'YApMgSnw3kJIgSkwBabAFJgCU2AKTIHXy0yBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp'
    b'MAWmwKuoUmAKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAUe'
    b'nl8KTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYAo85boXmwJTYApMgXd6eykwBabAFHi5jhSY'
    b'AlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAK3'
    b'9lJgCkyBKTAFpsAUmAJTYApMgSlw/zcp8BTCoYXbQkiBKTAFpsAUmAJTYApMgSkwBabAFJgC'
    b'U2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwHsLIQWm'
    b'wBSYAlNgCkyBKTAFXi8zBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAKvokqBKTAF'
    b'psAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUeHh+KTAFpsAUmAJT'
    b'YApMgSkwBabAFJgCU2AKTIEp8JTrXmwKTIEpMAXe6e2lwBSYAlPg5TpSYApMgSkwBabAFJgC'
    b'U2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AK3NpLgSkwBabAFJgC'
    b'U2AKTIEpMAWmwP3fpMBTCIcWbgshBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJT'
    b'YApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmALvLYQUmAJTYApMgSkwBabA'
    b'FHi9zBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKvIoqBabAFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU+Dh+aXAFJgCU2AKTIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsBTrnuxKTAFpsAUeKe3lwJTYApMgZfrSIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJT'
    b'YApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKXBrLwWmwBSYAlNgCkyBKTAFpsAUmAL3'
    b'f5MCTyEcWrgthBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKvLcQUmAKTIEpMAWmwBSYAlPg9TJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKfAqqhSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabA'
    b'FJgCU2AKTIEpMAWmwBSYAlNgCkyBh+eXAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCT7nu'
    b'xabAFJgCU+Cd3l4KTIEpMAVeriMFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsAUmAJTYApMgSkwBabArb0UmAJTYApMgSkwBabAFJgCU2AK3P9NCjyFcGjhthBS'
    b'YApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYAlNgCkyBKfDeQkiBKTAFpsAUmAJTYApMgdfLTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYApMgSkwBabAq6hSYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAU'
    b'mAJTYApMgSkwBR6eXwpMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCjzluhebAlNgCkyBd3p7'
    b'KTAFpsAUeLmOFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYArf2UmAKTIEpMAWmwBSYAlNgCkyBKXD/NynwFMKhhdtCSIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApM'
    b'gSkwBabAewshBabAFJgCU2AKTIEpMAVeLzMFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWm'
    b'wBSYAq+iSoEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBR4'
    b'eH4pMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSnwlOtebApMgSkwBd7p7aXAFJgCU+DlOlJg'
    b'CkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYArc'
    b'2kuBKTAFpsAUmAJTYApMgSkwBabA/d+kwFMIhxZuCyEFpsAUmAJTYApMgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAu8thBSY'
    b'AlNgCkyBKTAFpsAUeL3MFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYAq8iioFpsAU'
    b'mAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJT4OH5pcAUmAJTYApM'
    b'gSkwBabAFJgCU2AKTIEpMAWmwFOue7EpMAWmwBR4p7eXAlNgCkyBl+tIgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpcGsvBabAFJgCU2AK'
    b'TIEpMAWmwBSYAvd/kwJPIRxauC2EFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApM'
    b'gSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYAq8txBSYApMgSkwBabAFJgC'
    b'U+D1MlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp8CqqFJgCU2AKTIEpMAWmwBSY'
    b'AlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIGH55cCU2AKTIEpMAWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJPue7FpsAUmAJT4J3eXgpMgSkwBV6uIwWmwBSYAlNgCkyBKTAFpsAUmAJTYApM'
    b'gSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsCtvRSYAlNgCkyBKTAFpsAUmAJTYArc'
    b'/00KPIVwaOG2EFJgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp8N5CSIEpMAWmwBSYAlNgCkyB18tMgSkwBabA'
    b'FJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsCrqFJgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgC'
    b'U2AKTIEpMAWmwBSYAlNgCkyBKTAFHp5fCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKPOW6'
    b'F5sCU2AKTIF3enspMAWmwBR4uY4UmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJTYApMgSkwBabAFJgCt/ZSYApMgSkwBabAFJgCU2AKTIEpcP83KfAUwqGF20JI'
    b'gSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp'
    b'MAWmwBSYAlNgCkyBKTAFpsB7CyEFpsAUmAJTYApMgSkwBV4vMwWmwBSYAlNgCkyBKTAFpsAU'
    b'mAJTYApMgSkwBabAFJgCr6JKgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJT'
    b'YApMgSkwBabAFHh4fikwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKfCU615sCkyBKTAF3unt'
    b'pcAUmAJT4OU6UmAKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp'
    b'MAWmwBSYAlNgCtzaS4EpMAWmwBSYAlNgCkyBKTAFpsD936TAUwiHFm4LIQWmwBSYAlNgCkyB'
    b'KTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkw'
    b'BabAFJgC7y2EFJgCU2AKTIEpMAWmwBR4vcwUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSY'
    b'AlNgCryKKgWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlPg'
    b'4fmlwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAU657sSkwBabAFHint5cCU2AKTIGX60iB'
    b'KTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSlw'
    b'ay8FpsAUmAJTYApMgSkwBabAFJgC93+TAk8hHFq4LYQUmAJTYApMgSkwBabAFJgCU2AKTIEp'
    b'MAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCry3EFJg'
    b'CkyBKTAFpsAUmAJT4PUyU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSnwKqoUmAJT'
    b'YApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgYfnlwJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAk+57sWmwBSYAlPgnd5eCkyBKTAFXq4jBabAFJgCU2AKTIEp'
    b'MAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwK29FJgCU2AKTIEp'
    b'MAWmwBSYAlNgCtz/TQo8hXBo4bYQUmAKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSnw3kJIgSkwBabAFJgCU2AK'
    b'TIHXy0yBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwKuoUmAKTIEpMAWmwBSYAlNg'
    b'CkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAUenl8KTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYAo85boXmwJTYApMgXd6eykwBabAFHi5jhSYAlNgCkyBKTAFpsAUmAJTYApMgSkw'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAK39lJgCkyBKTAFpsAUmAJTYApMgSlw'
    b'/zcp8BTCoYXbQkiBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWmwHsLIQWmwBSYAlNgCkyBKTAFXi8zBabAFJgC'
    b'U2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAKvokqBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AK'
    b'TIEpMAWmwBSYAlNgCkyBKTAFpsAUeHh+KTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEp8JTr'
    b'XmwKTIEpMAXe6e2lwBSYAlPg5TpSYApMgSkwBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAF'
    b'psAUmAJTYApMgSkwBabAFJgCU2AK3NpLgSkwBabAFJgCU2AKTIEpMAWmwP3fpMBTCIcWbgsh'
    b'BabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApMgSkwBabAFJgCU2AKTIEpMAWm'
    b'wBSYAlNgCkyBKTAFpsAUmALvLYQUmAJTYApMgSkwBabAFHi9zBSYAlNgCkyBKTAFpsAUmAJT'
    b'YApMgSkwBabAFJgCU2AKvIoqBabAFJgCU2AKTIEpMAWmwBSYAlNgCkyBKTAFpsAUmAJTYApM'
    b'gSkwBabAFJgCU+Dh+aXAFJgCU2AKTIEpMAWmwBSYAlNgCkyBh2Znv38DafWwyFC5X1UAAAAA'
    b'SUVORK5CYII=')




class GradientPanel(wx.Panel):


    """This is a dynamic panel used to draw both the saturation and
    value gradients used in the editing preview."""
    
    def __init__(self, parent, hue=0, gradient_type="saturation"):
        
        super().__init__(parent)
        
        self.gradient_type = gradient_type
        self.hue = hue

        self.Bind(wx.EVT_PAINT, self._on_paint)



        
    def SetHue(self, hue):
        self.hue = hue
        self.Refresh()


        

    def _on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        width, height = self.GetSize()

        # create a gradient image based on the type
        if self.gradient_type == "saturation":
            gradient = np.zeros((height, width, 3), dtype=np.uint8)
            for x in range(width):
                saturation = int((x / width) * 255)
                gradient[:, x, :] = [self.hue, saturation, 255]

        elif self.gradient_type == "value":
            gradient = np.zeros((height, width, 3), dtype=np.uint8)
            for x in range(width):
                value = int((x / width) * 255)
                gradient[:, x, :] = [self.hue, 255, value]

        else:
            raise ValueError("GradientPanel::Invalid gradient type.")
                

        rgb_gradient = cv2.cvtColor(gradient, cv2.COLOR_HSV2RGB)

        image = wx.Image(width, height, rgb_gradient.tobytes())
        bitmap = wx.Bitmap(image)

        dc.DrawBitmap(bitmap, 0, 0)


        

class PanelHueImage(wx.Panel):

    """This panel is used to draw the hue_image in the paint event,
    stretching it while mantaining height (and also drawing with
    buffered dc)."""
    
    def __init__(self, parent, image:wx.Image, *args, **kwargs):
        
        super().__init__(parent, *args, **kwargs)

        self.image = image

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self._on_paint)



        
    def _on_paint(self, event):

        # get drawing contexts
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()

        gcdc.Clear()

        rect:wx.Rect = self.GetClientRect()

        bitmap = self.image.ConvertToBitmap()
        bitmap.SetSize(rect.GetSize())
        
        gcdc.DrawBitmap(bitmap, 0, 0)
        

        

class HSVSliders(wx.Panel):

    """This panel holds the color previews and sliders to adjust HSV
    values. Used to adjust both the lower and the upper boundaries.
    """
    
    def __init__(self, parent, config, lower, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config = config
        self.lower = lower

        self.SetBackgroundColour(wx.WHITE)

        if self.lower:
            hue = self.config.hsvEditLower[0]
            saturation = self.config.hsvEditLower[1]
            value = self.config.hsvEditLower[2]
        else:
            hue = self.config.hsvEditUpper[0]
            saturation = self.config.hsvEditUpper[1]
            value = self.config.hsvEditUpper[2]

        # create sizer to self
        self.sizer = wx.GridBagSizer()
        self.SetSizer(self.sizer)

        # -------------------- create elements -------------------- #
        
        image_hue_wximage = wx.Image(image_hue.GetImage())
        image_panel = PanelHueImage(self, image_hue_wximage)
        image_panel.SetMinClientSize(dip(-1, 30))

        self.saturation_panel = GradientPanel(self, gradient_type="saturation")
        self.saturation_panel.SetMinClientSize(dip(-1, 30))
        self.saturation_panel.SetHue(hue)
        self.value_panel = GradientPanel(self, gradient_type="value")
        self.value_panel.SetMinClientSize(dip(-1, 30))
        self.value_panel.SetHue(hue)

        self.h_slider = wx.Slider(self, value=hue, minValue=0, maxValue=179)
        self.s_slider = wx.Slider(self, value=saturation, minValue=0, maxValue=255)
        self.v_slider = wx.Slider(self, value=value, minValue=0, maxValue=255)

        self.color_preview = wx.Panel(self, size=dip(-1, 10))
        self.color_preview.SetBackgroundColour(wx.Colour(255, 255, 255))

        # ----------------- add elements to sizer ----------------- #
        
        self.sizer.Add(wx.StaticText(self, label="Hue:"), pos=(0, 0))
        
        self.sizer.Add(image_panel, pos=(1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.h_slider, pos=(2, 0), flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self, label="Saturation:"), pos=(3, 0))
        self.sizer.Add(self.saturation_panel, pos=(4, 0), flag=wx.EXPAND)
        self.sizer.Add(self.s_slider, pos=(5, 0), flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self, label="Value:"), pos=(6, 0))
        self.sizer.Add(self.value_panel, pos=(7, 0), flag=wx.EXPAND)
        self.sizer.Add(self.v_slider, pos=(8, 0), flag=wx.EXPAND)
        
        self.sizer.Add(self.color_preview, pos=(9, 0), flag=wx.EXPAND)

        self.sizer.AddGrowableCol(0, 1)

        self.sizer.Layout()

        # ---------------------- bind events ---------------------- #

        self.h_slider.Bind(wx.EVT_SLIDER, self._on_slider)
        self.s_slider.Bind(wx.EVT_SLIDER, self._on_slider)
        self.v_slider.Bind(wx.EVT_SLIDER, self._on_slider)


        

    def _on_slider(self, event):

        """Updates the color of the preview panels when a slider value
        is changed."""
        
        hue = self.h_slider.GetValue()
        saturation = self.s_slider.GetValue()
        value = self.v_slider.GetValue()

        self.saturation_panel.SetHue(hue)
        self.value_panel.SetHue(hue)

        hsv_color = np.uint8([[[hue, saturation, value]]])
        rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)[0][0]

        self.color_preview.SetBackgroundColour(wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2]))
        self.color_preview.Refresh()

        # update config edit values
        if self.lower:
            self.config.hsvEditLower = (hue, saturation, value)
        else:
            self.config.hsvEditUpper = (hue, saturation, value)



            
    def GetHSV(self):
        
        """This is used when saving the lower and upper boundaries adjusted in the panel."""
        
        hue = self.h_slider.GetValue()
        saturation = self.s_slider.GetValue()
        value = self.v_slider.GetValue()
        return (hue, saturation, value)



class FrameEditBoundary(wx.Frame):

    """This frame is used to add or edit boundary values."""
    
    def __init__(self, parent, config, boundaryName, mode, mainFrame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config = config
        self.boundaryName = boundaryName
        self.mode = mode
        self.mainFrame = mainFrame

        # if in edit mode, use designated temporal attributes in config (not saved).
        if self.mode == "edit":
            self.config.hsvEditLower = tuple(self.config.hsvBounds[self.boundaryName]["lower"])
            self.config.hsvEditUpper = tuple(self.config.hsvBounds[self.boundaryName]["upper"])
        # if in add mode, use lowest and highest limits.
        else:
            self.config.hsvEditLower = (0, 0, 0)
            self.config.hsvEditUpper = (179, 255, 255)

        self.SetTitle(f"{self.mode.capitalize()} boundary...") # Add or Edit
        self.SetClientSize(dip(650, 500))

        self._init_ui()


        

    def _init_ui(self):

        # ----------------------- main panel ----------------------- #

        # this panel will hold both the edit preview and the panel
        # containing the lower and upper boundary limits adjuster.

        self.panelMain = wx.Panel(self)
        self.panelMain.SetBackgroundColour(wx.WHITE)
        self.sizerMain = wx.GridBagSizer()
        self.panelMain.SetSizer(self.sizerMain)

        # --------------------- preview panel  --------------------- #

        self.panelPreview = PanelPreviewSource(self.panelMain, self.config, True)
        self.panelPreview.SetSource(self.config.sourcePath)

        # -------------------- hsv limits panel -------------------- #

        self.panelBoundariesLowerUpper = wx.Panel(self.panelMain)
        self.sizerBoundariesLowerUpper = wx.GridBagSizer()
        self.panelBoundariesLowerUpper.SetSizer(self.sizerBoundariesLowerUpper)

        self.staticBoxLower = wx.StaticBox(self.panelBoundariesLowerUpper, label="Lower Boundary")
        self.sizerStaticBoxLower = wx.BoxSizer()
        self.staticBoxLower.SetSizer(self.sizerStaticBoxLower)
        self.slidersLower = HSVSliders(self.staticBoxLower, self.config, lower=True)
        self.sizerStaticBoxLower.Add(self.slidersLower, 1, wx.EXPAND|wx.ALL, border=dip(18))
        
        self.staticBoxUpper = wx.StaticBox(self.panelBoundariesLowerUpper, label="Upper Boundary")
        self.sizerStaticBoxUpper = wx.BoxSizer()
        self.staticBoxUpper.SetSizer(self.sizerStaticBoxUpper)
        self.slidersUpper = HSVSliders(self.staticBoxUpper, self.config, lower=False)
        self.sizerStaticBoxUpper.Add(self.slidersUpper, 1, wx.EXPAND|wx.ALL, border=dip(18))
        
        self.sizerBoundariesLowerUpper.Add(self.staticBoxLower, pos=(0, 0), flag=wx.EXPAND|wx.ALL, border=dip(8))
        self.sizerBoundariesLowerUpper.Add(self.staticBoxUpper, pos=(0, 1), flag=wx.EXPAND|wx.ALL, border=dip(8))

        self.sizerBoundariesLowerUpper.AddGrowableCol(0, 1)
        self.sizerBoundariesLowerUpper.AddGrowableCol(1, 1)
        self.sizerBoundariesLowerUpper.AddGrowableRow(0, 1)

        # --------------------- buttons panel --------------------- #

        panelButtons = wx.Panel(self.panelMain)
        sizerButtons = wx.BoxSizer(wx.HORIZONTAL)
        panelButtons.SetSizer(sizerButtons)

        self._buttonOk = wx.Button(panelButtons, label="Ok")
        self._buttonCancel = wx.Button(panelButtons, label="Cancel")

        self._buttonOk.Bind(wx.EVT_BUTTON, self._on_button_ok)
        self._buttonCancel.Bind(wx.EVT_BUTTON, self._on_button_cancel)

        sizerButtons.Add(self._buttonCancel, 0, wx.RIGHT, border=dip(5))
        sizerButtons.Add(self._buttonOk, 0)

        # ---------------- add panels to main sizer ---------------- #

        self.sizerMain.Add(self.panelPreview, pos=(0, 0), flag=wx.EXPAND)
        self.sizerMain.Add(self.panelBoundariesLowerUpper, pos=(1, 0), flag=wx.EXPAND)
        self.sizerMain.Add(panelButtons, pos=(2, 0), flag=wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT, border=dip(5))

        self.sizerMain.AddGrowableCol(0, 1)
        self.sizerMain.AddGrowableRow(0, 1)
        
        self.sizerMain.Layout()

        self.Bind(wx.EVT_CLOSE, self._on_close)


        

    def _on_button_ok(self, event):

        if self.mode == "add":
            varName = ""
            while varName.strip() == "":
                dlg = wx.TextEntryDialog(self, "Enter boundary name:", "Boundary Name", "")    
                if dlg.ShowModal() == wx.ID_CANCEL:
                    return
                varName = dlg.GetValue()
            self.config.activeBounds.append(varName)
        else:
            varName = self.boundaryName

        self.config.hsvBounds[varName] = {"lower": self.slidersLower.GetHSV(),
                                          "upper": self.slidersUpper.GetHSV()}

        self.Destroy()
        self.mainFrame._refresh_boundaries_panels()
        self.panelPreview.pause()
        self.mainFrame.panelPreview.resume()
        

        

    def _on_button_cancel(self, event):
        self.panelPreview.pause()
        self.Destroy()
        self.mainFrame.panelPreview.resume()


        

    def _on_close(self, event):
        self.panelPreview.pause()
        self.Destroy()
        self.mainFrame.panelPreview.resume()
    
