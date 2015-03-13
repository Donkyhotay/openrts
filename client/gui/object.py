class Object:
    def __init__(self):
        self.connects = {}
        self.__class__
    
    def connect(self,code,fnc,value):
        self.connects[code] = {'fnc':fnc,'value':value}
    
    def send(self,code,event=None):
        if code in self.connects:
            con = self.connects[code]
            con['fnc'](con['value'])
    
    def _event(self,e):
        self.send(e.type,e)
        self.event(e)
        
    def event(self,e): pass
