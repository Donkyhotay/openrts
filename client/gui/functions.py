import pygame

def action_open(value):
    "Scheduled to be deprecated."
    value.setdefault('x',None)
    value.setdefault('y',None)
    value['container'].open(value['window'],value['x'],value['y'])

def action_setvalue(value):
    "Scheduled to be deprecated.  Maybe."
    a,b = value
    b.value = a.value

def action_quit(value):
    "Scheduled to be deprecated."
    value.quit()

def action_exec(value):
    "Scheduled to be deprecated."
    exec(value['script'],globals(),value['dict'])

def render_box(s,box,r):
    x,y,w,h=r.x,r.y,r.w,r.h
    ww,hh=box.get_width()/3,box.get_height()/3
    xx,yy=x+w,y+h
    src = pygame.rect.Rect(0,0,ww,hh)
    dest = pygame.rect.Rect(0,0,ww,hh)
    
    
    s.set_clip(pygame.Rect(x+ww,y+hh,w-ww*2,h-hh*2))
    src.x,src.y = ww,hh
    for dest.y in xrange(y+hh,yy-hh,hh): 
        for dest.x in xrange(x+ww,xx-ww,ww): s.blit(box,dest,src)
    
    s.set_clip(pygame.Rect(x+ww,y,w-ww*3,hh))
    src.x,src.y,dest.y = ww,0,y
    for dest.x in xrange(x+ww,xx-ww*2,ww): s.blit(box,dest,src)
    dest.x = xx-ww*2
    s.set_clip(pygame.Rect(x+ww,y,w-ww*2,hh))
    s.blit(box,dest,src)
    
    s.set_clip(pygame.Rect(x+ww,yy-hh,w-ww*3,hh))
    src.x,src.y,dest.y = ww,hh*2,y+h-hh
    for dest.x in xrange(x+ww,xx-ww*2,ww): s.blit(box,dest,src)
    dest.x = xx-ww*2
    s.set_clip(pygame.Rect(x+ww,yy-hh,w-ww*2,hh))
    s.blit(box,dest,src)

    s.set_clip(pygame.Rect(x,y+hh,xx,h-hh*3))
    src.y,src.x,dest.x = hh,0,x
    for dest.y in xrange(y+hh,yy-hh*2,hh): s.blit(box,dest,src)
    dest.y = yy-hh*2
    s.set_clip(pygame.Rect(x,y+hh,xx,h-hh*2))
    s.blit(box,dest,src)

    s.set_clip(pygame.Rect(xx-ww,y+hh,xx,h-hh*3))
    src.y,src.x,dest.x=hh,ww*2,x+w-ww
    for dest.y in xrange(y+hh,yy-hh*2,hh): s.blit(box,dest,src)
    dest.y = yy-hh*2
    s.set_clip(pygame.Rect(xx-ww,y+hh,xx,h-hh*2))
    s.blit(box,dest,src)
    
    s.set_clip()
    src.x,src.y,dest.x,dest.y = 0,0,x,y
    s.blit(box,dest,src)
    
    src.x,src.y,dest.x,dest.y = ww*2,0,x+w-ww,y
    s.blit(box,dest,src)
    
    src.x,src.y,dest.x,dest.y = 0,hh*2,x,y+h-hh
    s.blit(box,dest,src)
    
    src.x,src.y,dest.x,dest.y = ww*2,hh*2,x+w-ww,y+h-hh
    s.blit(box,dest,src)

def mysubsurface(s,r):
    r = pygame.Rect(r)
    if r.x < 0 or r.y < 0:
        raise "_subsurface: %d %d %s"%(s.get_width(),s.get_height(),r)
    w,h = s.get_width(),s.get_height()
    if r.right > w:
        r.w -= r.right-w
    if r.bottom > h:
        r.h -= r.bottom-h
    return s.subsurface(r)
