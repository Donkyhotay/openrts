import pygame
import widget
import client.tileset as tileset

class Image(widget.Widget):
    def __init__(self,value,**params):
        widget.Widget.__init__(self,**params)
        if type(value) == str: value = tileset.load(value)
        self.value = value
        self.style.width = self.value.get_width()
        self.style.height = self.value.get_height()
        self.style.disabled = 1
    
    def paint(self,s):
        s.blit(self.value,(0,0))
