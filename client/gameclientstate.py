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

from mapview import *
from mapctrl import *
from mappanel import *
from networkclient import *
from tileset import *
from twisted.internet import task, reactor

from common.map import * 
from common.mapgen import *
from common.settings import *
from common.ruleset import *
from common.game import *
from server.main import *

#****************************************************************************
#
#****************************************************************************
class GameClientState:
  def __init__(self):


    self.settings = GameSettings();
    self.screen_width = self.settings.screen_width;
    self.screen_height = self.settings.screen_height;
    self.screen = None;

    self.map = Map(self);
    self.mappanel = None;
    self.pregame = None;
    self.tileset = Tileset(self);
    self.ruleset = None;
    self.game = None;
    self.clock = pygame.time.Clock();
    self.fps = 40;
    self.loop = task.LoopingCall(self.mainloop);



#****************************************************************************
#
#****************************************************************************
  def mainloop(self):
    self.clock.tick(self.fps);

    self.mapview.drawmap();
    self.mapctrl.handle_events();
    self.mappanel.draw_minimap();
    pygame.display.flip();
 

#****************************************************************************
#
#****************************************************************************
  def host_network_game(self, address, username):
    #Start a new server.
    srv = ServerMain();
    srv.start_from_client();

    #wait, then connect to the server.
    pygame.time.wait(50);

    self.connect_network_game(address, username);

#****************************************************************************
#
#****************************************************************************
  def game_next_phase(self):
    if self.game:
      self.game.game_next_phase();

#****************************************************************************
#
#****************************************************************************
  def connect_network_game(self, address, username):

    self.username = username;
    self.netclient = NetworkClient(self); 
    self.netclient.connect(address, 9071, username);

#****************************************************************************
#
#****************************************************************************
  def start_game(self):
    logging.info("Init game state")
    self.game = Game(self.map, self.ruleset);

    self.tileset.load_tileset();
    self.mapctrl = Mapctrl(self);
    self.mappanel = Mappanel(self);
    self.mapview = Mapview(self);
    self.loop.start(1.0/self.fps);
    self.mappanel.show_message("The game has started.");


#****************************************************************************
#
#****************************************************************************
  def load_ruleset(self, name):
    ruleset_src = self.settings.get_ruleset_src(name);
    self.ruleset = Ruleset(ruleset_src);

#****************************************************************************
#
#****************************************************************************
  def quit(self):
    if reactor.running:
      reactor.stop();
    if self.mappanel:
      self.mappanel.app.quit();
    pygame.quit();
    sys.exit(0);
 
#****************************************************************************
#
#****************************************************************************
  def enter_pregame(self):
    import networkscreen 
    self.pregame = networkscreen.PregameScreen(self); 


