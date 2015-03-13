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
import pygame
import gettext

import introscreen  

from networkclient import *
from gameclientstate import *
from mainmenu import *

from common.translation import *


#****************************************************************************
# The Main class of the client. 
#****************************************************************************
class Main:

  def __init__(self):
    pygame.init();
  
    self.gameclient = GameClientState();    
    logging.info("OpenRTS %s" % (self.gameclient.settings.version));
    if self.gameclient.settings.psyco:
      try:
        import psyco
        logging.info('Enabled "psyco" just-in-time Python compiler.')
        psyco.full()
      except ImportError:
        logging.info('"Psyco" just-in-time Python compiler not found.');


    self.initialize_locale();

    self.create_main_window();
    self.intro = introscreen.IntroScreen(self.gameclient.screen);

    mainmenu = MainMenu(self.gameclient);

#****************************************************************************
#
#****************************************************************************
  def initialize_locale(self):
    translation = Translation();
    translation.setLanguage(self.gameclient.settings.language)

#****************************************************************************
#
#****************************************************************************
  def create_main_window(self):
    screen_width = self.gameclient.settings.screen_width; 
    screen_height = self.gameclient.settings.screen_height; 

    if (self.gameclient.settings.fullscreen):
      screen_mode = pygame.FULLSCREEN;
    else:
      screen_mode = 0;
    screen = pygame.display.set_mode((screen_width, screen_height), screen_mode);

    pygame.display.set_caption("OpenRTS %s" % (self.gameclient.settings.version));
    self.gameclient.screen = screen;


