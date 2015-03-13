import table, group, label, button, image
from base import *

class Toolbox(table.Table):
    def __setattr__(self,k,v):
        _v = self.__dict__.get(k,NOATTR)
        self.__dict__[k]=v
        if k == 'value' and _v != NOATTR and _v != v: 
            self.group.value = v
            for w in self.group.widgets:
                if w.value != v: w.pcls = ""
                else: w.pcls = "down"
            self.repaint()
    
    def _change(self,value):
        self.value = self.group.value
        self.send(CHANGE)
    
    def __init__(self,data,cols=0,rows=0,tool_cls='tool',value=None,**params):
        params.setdefault('cls','toolbox')
        table.Table.__init__(self,**params)
        
        if cols == 0 and rows == 0: cols = len(data)
        if cols != 0 and rows != 0: rows = 0
        
        self.tools = {}
        
        _value = value
        
        g = group.Group()
        self.group = g
        g.connect(CHANGE,self._change,None)
        self.group.value = _value
        
        x,y,p,s = 0,0,None,1
        for ico,value in data:
            #from __init__ import theme
            import app
            img = app.App.app.theme.get(tool_cls+"."+ico,"","image")
            if img:
                i = image.Image(img)
            else: i = label.Label(ico,cls=tool_cls+".label")
            p = button.Tool(g,i,value,cls=tool_cls)
            self.tools[ico] = p
            #p.style.hexpand = 1
            #p.style.vexpand = 1
            self.add(p,x,y)
            s = 0
            if cols != 0: x += 1
            if cols != 0 and x == cols: x,y = 0,y+1
            if rows != 0: y += 1
            if rows != 0 and y == rows: x,y = x+1,0
