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

import os, sys
import string
import os, os.path
from xml.dom import minidom, Node

import logging


#****************************************************************************
#  This class reads game settings from a XML file.
#****************************************************************************
class GameSettings:

  def __init__(self):
    filename = os.path.join('data', 'settings.xml');
    self.rulesets = {};

    doc = minidom.parse(filename);
    rootNode = doc.documentElement;

    settingNode = rootNode.getElementsByTagName('openrts').item(0);
    self.version = settingNode.getAttribute('version');

    settingNode = rootNode.getElementsByTagName('fullscreen').item(0);
    self.fullscreen = settingNode.getAttribute('enabled') == 'true';

    settingNode = rootNode.getElementsByTagName('tileset').item(0);
    self.tileset = settingNode.getAttribute('src');

    settingNode = rootNode.getElementsByTagName('ruleset_default').item(0);
    self.ruleset_name = settingNode.getAttribute('name');

    for settingNode in rootNode.getElementsByTagName('ruleset'):
      rulesetname = settingNode.getAttribute('name');
      rulesetsrc = settingNode.getAttribute('src');
      self.rulesets.update({rulesetname:rulesetsrc});

    settingNode = rootNode.getElementsByTagName('screen').item(0);
    self.screen_width = int(settingNode.getAttribute('width'));
    self.screen_height = int(settingNode.getAttribute('height'));

    settingNode = rootNode.getElementsByTagName('language').item(0);
    self.language = settingNode.getAttribute('locale');

    settingNode = rootNode.getElementsByTagName('psyco-jit').item(0);
    self.psyco = settingNode.getAttribute('enabled') == 'true';


  def get_ruleset_src(self, rulesetname):
    return self.rulesets[rulesetname];


