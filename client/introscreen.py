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

import os
import pygame
import logging
import tileset

#****************************************************************************
#  The Introscreen shows a splash image. FIXME: Video, sound etc...
#****************************************************************************

class IntroScreen:
  def __init__(self, screen):
    filename = os.path.join('data', 'graphics', 'intro.png');
    surface = tileset.load(filename);
    scale = float(screen.get_width()) / surface.get_width();
    intro = pygame.transform.rotozoom(surface, 0, scale);
    screen.blit(intro, (0,0));
    pygame.display.flip();
    pygame.time.delay(1500);

