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

import sys, os

import pygame
from pygame.locals import *
import gui
import gettext
from random import *

from networkscreen import *
import tileset

#****************************************************************************
# The MainMenu class shows buttons with choices for what game-mode
# which will be used.
#****************************************************************************
class MainMenu:
  def __init__(self, client):

    self.client = client;
    self.app = gui.Desktop();
    self.app.connect(gui.QUIT, self.app.quit, None);
    container = gui.Container(align=-1, valign=-1);

    menu_table = gui.Table(width=200,height=220);
    network_start_button = gui.Button(_("Start Multiplayer Game"));
    network_start_button.connect(gui.CLICK, self.network_start, None);
    menu_table.add(network_start_button, 0, 0);
    menu_table.add(gui.Widget(width=1, height=5), 0, 1);

    network_join_button = gui.Button(_("Join Multiplayer Game"));
    network_join_button.connect(gui.CLICK, self.network_join, None);
    menu_table.add(network_join_button, 0, 2);
    menu_table.add(gui.Widget(width=1, height=5), 0, 3);

    single_button = gui.Button(_("Start Singleplayer Game"));
    menu_table.add(single_button, 0, 4);
    menu_table.add(gui.Widget(width=1, height=5), 0, 5);

    settings_button = gui.Button(_("Settings"));
    menu_table.add(settings_button, 0, 6);
    menu_table.add(gui.Widget(width=1, height=5), 0, 7);

    credits_button = gui.Button(_("Credits"));
    menu_table.add(credits_button, 0, 8);
    menu_table.add(gui.Widget(width=1, height=5), 0, 9);

    quit_button = gui.Button(_("Quit"));
    quit_button.connect(gui.CLICK, self.client.quit);
    menu_table.add(quit_button, 0, 10);

    intro_label = gui.Label(_("Open Source Real-Time Strategy Game"));
    tip_label = gui.Label(_("Tip of the day:"));

    container.add(MenuBackground(client=self.client, 
                   width = self.client.screen.get_width(),
                   height = self.client.screen.get_height()), 0, 0);
    container.add(menu_table, self.client.screen.get_width() / 2 - 100,
                              self.client.screen.get_height() / 2 - 100);
    container.add(intro_label, self.client.screen.get_width() / 2 - 160,
                              self.client.screen.get_height() * 0.315);
    container.add(tip_label, self.client.screen.get_width() * 0.3,
                              self.client.screen.get_height() * 0.71);
    container.add(self.get_tip_of_the_day(), self.client.screen.get_width() * 0.3,
                              self.client.screen.get_height() * 0.74);

    self.app.run(container);

#****************************************************************************
#  Each tip must not be more than 80 characters (fit on one line). 
#****************************************************************************
  def get_tip_of_the_day(self):
    tips = [];
    tips.append(_("To get updates of OpenRTS, visit www.openrts.org."));
    tips.append(_("OpenRTS is licensed under the GNU General Public License."));
    tips.append(_("The game can be translated to several languages."));
    return gui.Label(choice(tips)); 

#****************************************************************************
#  Start a network game.
#****************************************************************************
  def network_start(self, obj):
    self.app.quit();
    ns = NetworkScreen(self.client);
    ns.start();

#****************************************************************************
#  Join a network game.
#****************************************************************************
  def network_join(self, obj):
    self.app.quit();
    ns = NetworkScreen(self.client);
    ns.join();
 
#****************************************************************************
#
#****************************************************************************
class ErrorMenu:
  def __init__(self, client, error_message):

    self.client = client;
    self.app = gui.Desktop();
    self.app.connect(gui.QUIT, sys.exit, None);

    menu_table = gui.Table(width=200,height=120);
    error_label = gui.Label(error_message);
    menu_table.add(error_label, 0, 0);

    accept_button = gui.Button(_("OK"));
    menu_table.add(accept_button, 0, 1);
    accept_button.connect(gui.CLICK, self.recover, None);

    self.app.run(menu_table);

#****************************************************************************
#  Return to main menu.
#****************************************************************************
  def recover(self, obj):
    self.app.quit();
    MainMenu(self.client);

#****************************************************************************
#
#****************************************************************************
class MenuBackground(gui.Widget):
  def __init__(self,**params):
    gui.Widget.__init__(self,**params)
    client = params['client'];
    filename = os.path.join('data', 'graphics', 'menubackground.jpg');
    surface = tileset.load(filename);
    scale = float(client.screen.get_width()) / surface.get_width();
    self.surface = pygame.transform.rotozoom(surface, 0, scale);

#****************************************************************************
#
#****************************************************************************
  def paint(self,s):
    s.blit(self.surface,(0,0));


