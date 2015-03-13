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
from twisted.internet import reactor
from twisted.spread import pb
from twisted.cred.credentials import UsernamePassword
import cPickle
import zlib

#****************************************************************************
#
#****************************************************************************
class NetworkClient(pb.Referenceable):
  def __init__(self, clientstate):
    self.perspective = None
    self.client = clientstate;

#****************************************************************************
# Todo: Add error handling
#****************************************************************************
  def network_handle(self, string):
    data = zlib.decompress(string);
    object = cPickle.loads(data);
    return object;

#****************************************************************************
#
#****************************************************************************
  def network_prepare(self, object):
    data = cPickle.dumps(object);
    compressed = zlib.compress(data);
    return compressed;


#****************************************************************************
#
#****************************************************************************
  def connect(self, server, serverPort, username):
    self.server = server;
    self.serverPort = serverPort;
    self.username = username;
    factory = pb.PBClientFactory();
    reactor.connectTCP("localhost", 9071, factory)
    df = factory.login(UsernamePassword("guest", "guest"), self);
    df.addCallback(self.connected);
    reactor.run();
    
  def start_server_game(self):
    self.perspective.callRemote('init_game')

  def success(self, message):
    logging.info("Message received: %s" % message);

  def failure(self, error):
    logging.info("error received:");
    reactor.stop();

  def connected(self, perspective):
    self.perspective = perspective
    perspective.callRemote('login', self.username, self.client.settings.version).addCallback(self.login_result)
    logging.info("connected.");

  def login_result(self, result):
    if result == "login_accept":
      logging.info("Server accepted login");
      self.client.enter_pregame();   
    else:
      logging.info("Server denied login");   


  def send_chat(self, message):
    data = self.network_prepare(message);
    self.perspective.callRemote('send_chat', data);

  def send_unit_path(self, unit, path):
    net_unit = self.network_prepare(unit);
    net_path = self.network_prepare(path);
    self.perspective.callRemote('send_unit_path', unit, path);


  def error(self, failure, op=""):
    logging.info('Error in %s: %s' % (op, str(failure.getErrorMessage())))
    if reactor.running:
      reactor.stop();


  # Methods starting with remote_ can be called by the server.
  def remote_chat(self, message):
    if self.client.mappanel:
      self.client.mappanel.show_message(message);
    if self.client.pregame:
      self.client.pregame.show_message(message);

  def remote_network_sync(self):
    logging.info("* Network sync");
    self.client.game_next_phase();

  def remote_unit_list(self, net_unit_list):
    self.client.map.unitstore = self.network_handle(net_unit_list);

  def remote_map(self, net_map):
    self.client.map.mapstore = self.network_handle(net_map);

  def remote_start_client_game(self):
    self.client.pregame.start_game();

  def remote_unit_path(self, net_unit, net_path):
    path = self.network_handle(net_path);
    unit_id = self.network_handle(net_unit);
    unit = self.client.map.get_unit_from_id(unit_id);
    unit.path = path;

