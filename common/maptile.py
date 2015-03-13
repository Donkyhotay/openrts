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

#****************************************************************************
#
#****************************************************************************
class MapTile:
  def __init__(self, type, x, y):
    self.x = x;
    self.y = y;
    self.type = type;  

#****************************************************************************
# Test for equality with tile. Must be implemented for pathfinding
#****************************************************************************
  def __eq__(self, tile):
    if tile == None: 
      return 0;
  
    if tile.x == self.x and tile.y == self.y:
      return 1;
    else:
      return 0;

