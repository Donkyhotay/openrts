#!/usr/bin/python2.4

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

import logging
import platform
import sys

import common.log

#****************************************************************************
# Check dependencies (Pygame).
#****************************************************************************
def dependencyCheck():
  logging.info('Platform: ' + platform.platform());
  logging.info('Python version ' + sys.version);
  try:
    import pygame;
    logging.info('Pygame version: ' + pygame.version.ver);
  except ImportError, err:
    logging.error('Loading dependency "pygame" failed: ' + str(err));
    sys.exit(1);
  try :
    import Image
    logging.info('Python Image Library version ' + Image.VERSION);
  except ImportError, err:
    logging.error('Loading dependency "PIL" failed: ' + str(err));
    sys.exit(1);
  try:
    import twisted
    if hasattr(twisted, '__version__'):
      logging.info('Twisted version ' + twisted.__version__)
    else:
      logging.debug('Twisted version unknown (probably old)')
  except ImportError, err:
    logging.error('Loading dependency "twisted" failed: ' + str(err))
    sys.exit(1)


def main():

  #logLevel = logging.WARNING
  logLevel = logging.INFO
  common.log.setUpLogging(logLevel);

  dependencyCheck();
  import client.main;
  client = client.main.Main()

main();


