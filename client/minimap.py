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
import Image, ImageDraw

import tileset

#****************************************************************************
# The Minimap is a _mini_ map. 
#****************************************************************************
class Minimap:

  def __init__(self, clientstate, x, y, width, height):
    self.client = clientstate;
    self.width = width;
    self.height = height;
    self.x = x;
    self.y = y;

    self.count = 0;

#****************************************************************************
# Updates the minimap. 
#****************************************************************************
  def update(self):
    #self.count += 1;
    # FIXME: This updates every 60th frame. Should only update when new info.
   # if (self.count % 60 != 1 and not force):
   #   return;
    terrain_data = [];
    resultimage = Image.new("RGBA", (self.width, self.height));
    mapimage = Image.new("RGBA", (self.client.map.xsize,
                                  self.client.map.ysize));

    for y in range(self.client.map.ysize):
      for x in range(self.client.map.xsize):
        tile = self.client.map.get_tile((x, y));
        if (tile.type.id == "ocean"):
          color = (12, 42, 130);
        elif (tile.type.id == "coast"):
          color = (12, 42, 170);
        else:
          #FIXME: color = (0, 180 - tile.height * 40, 50); 
          color = (0, 90, 50); 
        terrain_data.append(color);
 
    # Draw line showing where the current mapview view is.
    x1, y1 = self.client.mapview.canvas_to_map((0, 0));
    x2, y2 = self.client.mapview.canvas_to_map((self.client.screen_width, 0));
    x3, y3 = self.client.mapview.canvas_to_map((self.client.screen_width,
                                                self.client.screen_height));
    x4, y4 = self.client.mapview.canvas_to_map((0, self.client.screen_height));
    points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)];

    mapimage.putdata(terrain_data);
    drawer = ImageDraw.Draw(mapimage);

    if not (y4 < y2 or x1 > x3):
      drawer.line(points);

    for unit in self.client.map.get_unit_list():
      map_pos = self.client.map.get_unit_pos(unit); 
      drawer.point(map_pos, fill=(255,0,0));

    del drawer;
    resultimage = mapimage.resize((self.width, self.height), Image.ANTIALIAS);

    self.minimap_surface = pygame.image.fromstring(resultimage.tostring(), 
                                              resultimage.size, resultimage.mode);
  

#****************************************************************************
# Draws the entire minimap to the screen.
#****************************************************************************
  def draw(self):
    self.count += 1;
    # FIXME: This updates every 60th frame. Should only update when new info.
    if (self.count % 60 == 1 ):
      self.update();
    if not self.minimap_surface:
      self.update();
    self.client.screen.blit(self.minimap_surface, (self.x, self.y));


#****************************************************************************
# Handles mouse click events.
#****************************************************************************
  def handle_mouse_click(self, pos):
    (x, y) = pos;
    map_x = (x - self.x) * self.client.map.xsize / self.width;
    map_y = (y - self.y) * self.client.map.ysize / self.height;
    self.client.mapview.center_view_on_tile((map_x, map_y));
    self.update();

