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
from random import *
from common.map import *

#****************************************************************************
#
#****************************************************************************
class MapGen:
  def __init__(self, map, ruleset):
    self.map = map;
    self.ruleset = ruleset;
    self.waterlevel = 6
    self.maxheight = 20 

    logging.info("Generating a random new map");
    self.generate_heights();


#****************************************************************************
#
#****************************************************************************
  def generate_heights(self):
    heightmap_a = {};
    heightmap_b = {};

    # Randomly generate a heightmap
    for x in range(self.map.xsize):
      for y in range(self.map.ysize):
        heightmap_a[x,y] = randint(0, self.maxheight);

    # Gaussian blur operation on heightmap
    # with a 3x3 convolution matrix.
    for i in range(4):
      for x in range(self.map.xsize):
        for y in range(self.map.ysize):
          if (x == 0 or y == 0 or x+1== self.map.xsize or y+1 == self.map.ysize):
            heightmap_b[x,y] = 0;
            continue; 
          heightmap_b[x,y] = (heightmap_a[x-1,y] 
                              + heightmap_a[x+1,y] 
                              + heightmap_a[x,y-1] 
                              + heightmap_a[x,y+1]
                              + heightmap_a[x+1,y+1]
                              + heightmap_a[x-1,y-1]
                              + heightmap_a[x-1,y+1]
                              + heightmap_a[x+1,y-1]
                               ) / 8;
      heightmap_a = heightmap_b;    

    # Subtract heightmap with waterlevel.
    for x in range(self.map.xsize):
      for y in range(self.map.ysize):
        if (heightmap_a[x,y] < self.waterlevel):
          heightmap_a[x,y] = self.waterlevel;
        heightmap_a[x,y] -= self.waterlevel;

    # Create terrain types oceans and plains
    for x in range(self.map.xsize):
      for y in range(self.map.ysize):
        tile = self.map.get_tile((x, y));
        if (int(heightmap_a[x,y]) == 0):
          tile.type = self.ruleset.get_terrain_type('ocean');
        else:
          tile.type = self.ruleset.get_terrain_type('plains');
