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

from common.map import * 
from common.unit import * 


#****************************************************************************
#
#****************************************************************************
class Game:
  def __init__(self, map, ruleset):
    self.map = map;
    self.ruleset = ruleset;
    self.time = 0;
    self.unit_counter = 0;

#****************************************************************************
#
#****************************************************************************
  def game_next_phase(self):
    self.time = (self.time + 1) % 1024;
    self.move_units();

#****************************************************************************
#
#****************************************************************************
  def move_units(self):
   for unit in self.map.get_unit_list():
     self.map.move_unit(unit); 

#****************************************************************************
#
#****************************************************************************
  def create_unit(self, unit_type_id, pos):
    self.unit_counter += 1;
    drone_type = self.ruleset.get_unit_type(unit_type_id);
    self.map.set_unit(Unit(self.unit_counter, drone_type), pos);

