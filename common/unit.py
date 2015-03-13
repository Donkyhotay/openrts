#
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

import logging

#****************************************************************************
#
#****************************************************************************
class Unit:
  def __init__(self, id, type):
    self.id = id;
    self.type = type;       
    self.dir = 3;
    self.owner = None;
    self.path = None;
    self.x = 0;
    self.y = 0;
    self.offset = (0,0);
    self.speed = (0,0);

#****************************************************************************
#
#****************************************************************************
  def calc_dir(self, new_x, new_y):
    if new_x == self.x - 1 and new_y == self.y:
      self.dir = 3;
      self.offset = (0.5, 0.5);
    if new_x == self.x and new_y == self.y - 1:
      self.dir = 1;
      self.offset = (-0.5, 0.5);
    if new_x == self.x + 1 and new_y == self.y - 1:
      self.dir = 0;
      self.offset = (-1.0, 0.0);
    if new_x == self.x - 1 and new_y == self.y - 1:
      self.dir = 2;
      self.offset = (0.0, 1.0);
    if new_x == self.x - 1 and new_y == self.y + 1:
      self.dir = 4;
      self.offset = (1.0, 0);
    if new_x == self.x and new_y == self.y + 1:
      self.dir = 5;
      self.offset = (0.5, -0.5);
    if new_x == self.x + 1 and new_y == self.y + 1:
      self.dir = 6;
      self.offset = (0.0, -1.0);
    if new_x == self.x + 1 and new_y == self.y:
      self.dir = 7; 
      self.offset = (-0.5, -0.5);
    ox, oy = self.offset;
    self.speed = (-ox, -oy);
    #logging.info("unit dir %r" % (self.dir));
    #logging.info(self.offset);
