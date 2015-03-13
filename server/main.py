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
import time
import pygame

from gameserverstate import *

#****************************************************************************
#
#****************************************************************************
class ServerMain:
  def __init__(self):
    self.serverstate = ServerState();

    #Enable Psyco, if found.
    if self.serverstate.settings.psyco:
      try:
        import psyco;
        psyco.full();
      except ImportError:
        pass; 

#****************************************************************************
#
#****************************************************************************
  def start_from_client(self):
    self.serverstate.setup_network();

#****************************************************************************
#
#****************************************************************************
  def start_from_server(self):
    self.serverstate.setup_network();
    self.serverstate.run_network();

 

