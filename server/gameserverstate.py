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
from twisted.internet import task, reactor
from twisted.cred.portal import Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.spread import pb
from twisted.cred.portal import IRealm

from common.map import * 
from common.game import * 
from common.mapgen import *
from common.settings import *
from common.ruleset import *
from connectionhandler import *


#****************************************************************************
#
#****************************************************************************
class ServerState:
  def __init__(self):
    self.settings = GameSettings();
    self.game = None; 

 
#****************************************************************************
#
#****************************************************************************
  def setup_new_game(self):

    if not self.game:
      self.map = Map(self);
      ruleset_src = self.settings.get_ruleset_src(self.settings.ruleset_name);
      self.ruleset = Ruleset(ruleset_src);
      self.game = Game(self.map, self.ruleset);

      MapGen(self.map, self.ruleset);

      #FIXME: These are just for tests.

      self.game.create_unit('drone', (20,22));
      self.game.create_unit('drone', (25,25));
      self.game.create_unit('drone', (40,12));
      self.game.create_unit('drone', (70,80));
      self.game.create_unit('drone', (64,82));

      #Initialize main loop callback.
      self.loop = task.LoopingCall(self.mainloop);
      self.loop.start(1.0);


#****************************************************************************
# This method is called every second.
#****************************************************************************
  def mainloop(self):
    self.connections.remote_all('network_sync');

#****************************************************************************
#
#****************************************************************************
  def setup_network(self):
    self.connections = ConnectionHandler(self)
    portal = Portal(self.connections);
    checker = InMemoryUsernamePasswordDatabaseDontUse();
    checker.addUser("guest", "guest");
    portal.registerChecker(checker);
    reactor.listenTCP(9071, pb.PBServerFactory(portal));

#****************************************************************************
#
#****************************************************************************
  def run_network(self):

    reactor.run();

