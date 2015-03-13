import pygame
import widget
from base import *

class Color(widget.Widget):
    def __init__(self,value=None,**params):
        if value != None: params['value']=value
        widget.Widget.__init__(self,**params)
        #self.value = value
    
    def paint(self,s):
        if hasattr(self,'value'): s.fill(self.value)
    
    def __setattr__(self,k,v):
        if k == 'value' and type(v) == str: v = pygame.Color(v)
        _v = self.__dict__.get(k,NOATTR)
        self.__dict__[k]=v
        if k == 'value' and _v != NOATTR and _v != v: 
            self.send(CHANGE)
            self.repaint()
