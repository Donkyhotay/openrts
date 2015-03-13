# OpenRTS - Copyright (C) 2006 The OpenRTS Project
#
# OpenRTS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# OpenRTS is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

import os, sys
import pygame
import time
import logging
from pygame.locals import *

#****************************************************************************
"""
This is a nice little GfxCursor class that gives you arbitrary mousecursor
loadable from all SDL_image supported filetypes. 

Author: Raiser, Frank aka CrashChaos (crashchaos at gmx.net)
Author: Shinners, Pete aka ShredWheat
Version: 2001-12-15

Usage:
Instantiate the GfxCursor class. Either pass the correct parameters to
the constructor or use setCursor, setHotspot and enable lateron.

The blitting is pretty optimized, the testing code at the bottom of
this script does a pretty thorough test of all the drawing cases.
It enables and disables the cursor, as well as uses a changing background.

In your mainloop, the cursor.show() should be what you draw last
(unless you want objects on top of the cursor?). Then before drawing
anything, be sure to call the hide(). You can likely call hide() immediately
after the display.flip() or display.update().

The show() method also returns a list of rectangles of what needs to be
updated. You can also move the cursor with pygame.mouse.set_pos()

  surface = Global surface to draw on
  cursor  = surface of cursor (needs to be specified when enabled!)
  hotspot = the hotspot for your cursor


That's it. Have fun with your new funky cursors.
"""
#****************************************************************************
class GfxCursor:
    def __init__(self,client, surface, hotspot=(16,16), type=None):
        self.surface = surface;
        self.enabled = 0;
        self.cursor  = None;
        self.hotspot = hotspot;
        self.bg      = None;
        self.offset  = 0,0;
        self.old_pos = 0,0;
        self.client = client;
        self.type = type;
        
        if type:
            self.set_cursor_type(type);
            self.enable();

    def enable(self):
        """
        Enable the GfxCursor (disable normal pygame cursor)
        """
        if not self.cursor or self.enabled: return
        pygame.mouse.set_visible(0)
        self.enabled = 1

    def disable(self):
        """
        Disable the GfxCursor (enable normal pygame cursor)
        """
        if self.enabled:
            self.hide()
            pygame.mouse.set_visible(1)
            self.enabled = 0
            self.type = None;

    def set_cursor_surface(self,cursor,hotspot=(16,16)):
        """
        Set a new cursor surface
        """
        if not cursor: return
        self.cursor = cursor
        self.hide()
        self.show()
        self.offset = 0,0
        self.bg = pygame.Surface(self.cursor.get_size())
        pos = self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]
        self.bg.blit(self.surface,(0,0),
            (pos[0],pos[1],self.cursor.get_width(),self.cursor.get_height()))

        self.offset = hotspot

    def setHotspot(self,pos):
        """
        Set a new hotspot for the cursor
        """
        self.hide()
        self.offset = pos

    def hide(self):
        """
        Hide the cursor (useful for redraws)
        """
        if self.bg and self.enabled:
            return self.surface.blit(self.bg,
                (self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]))

    def show(self):
        """
        Show the cursor again
        """
        if self.bg and self.enabled:
            pos = self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]
            self.cursor = self.client.tileset.get_mouse_cursor(self.type);
            self.bg.blit(self.surface,(0,0),
                (pos[0],pos[1],self.cursor.get_width(),self.cursor.get_height()))
            return self.surface.blit(self.cursor,pos)

    def update(self,event):
        """
        Update the cursor with a MOUSEMOTION event
        """
        try:
          self.old_pos = event.pos
          x, y = event.pos;
        except: 
          pass

    def set_cursor_type(self, type):
       if type == 'default': 
         self.disable();
         return;
       self.type = type; 
       cursor = self.client.tileset.get_mouse_cursor(type);
       self.setHotspot((cursor.get_width()/2, cursor.get_height()/2));
       self.set_cursor_surface(cursor);
       self.enable();
