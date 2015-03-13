#!/usr/bin/env python 
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

def main():


  logLevel = logging.INFO
  common.log.setUpLogging(logLevel);

  logging.info("OpenRTS Server started.");


  import server.main;
  srv = server.main.ServerMain();
  srv.start_from_server();
  


main();


