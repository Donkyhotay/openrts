import widget

class Label(widget.Widget):
    def __init__(self,value,**params):
        params.setdefault('cls','label')
        widget.Widget.__init__(self,**params)
        self.value = value
        self.font = self.style.font
        self.style.width, self.style.height = self.font.size(self.value)
        self.style.disabled = 1
    
    def paint(self,s):
        s.blit(self.font.render(self.value, 1, self.style.color),(0,0))
