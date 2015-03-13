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

#****************************************************************************
#
#****************************************************************************
def setUpLogging(loglevel):
    # Add custom "debug2" level
    logging.setLoggerClass(CustomLogger);
    logging.addLevelName(9, "DEBUG2");
    
    # Create our stream handler
    console = logging.StreamHandler();
    formatter = logging.Formatter('%(name)-4s %(levelname)-8s %(message)s');
    console.setFormatter(formatter);
        
    # Set up all the logging streams
    for logger in ['', 'ai', 'gui', 'reso', 'batt']:
        logging.getLogger(logger).setLevel(loglevel);
        logging.getLogger(logger).addHandler(console);
        logging.getLogger(logger).propagate = False;

try:
    loggerClass = logging.getLoggerClass();
except AttributeError:
    loggerClass = logging.Logger;


#****************************************************************************
#
#****************************************************************************
class CustomLogger(loggerClass):
    def debug2(self, msg):
        self.log(9, msg);
