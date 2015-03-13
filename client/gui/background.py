import pygame
import widget
from functions import *

class Background(widget.Widget):
    def __init__(self,value,**params):
        params['decorate'] = False
        widget.Widget.__init__(self,**params)
        self.value = value
    
    def paint(self,s):
        r = pygame.Rect(0,0,s.get_width(),s.get_height())
        v = self.value.style.background
        if type(v) == tuple:
            s.fill(v)
        else: 
            render_box(s,v,r)
