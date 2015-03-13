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

import gettext, os

class Translation:

  def __init__(self):       
    #fill our language dictionnary with each language
    self.langDict= { 'no': self.getLanguageDict('no'),
		     'en': self.getLanguageDict('en')}; 
    #and install current langauge
    gettext.install('OpenRTS');
       

#****************************************************************************
#
#****************************************************************************   
  def getLanguageDict(self,lang):
    return gettext.translation('OpenRTS',os.path.join(os.getcwd(),'translations'), languages=[lang]);


#****************************************************************************
#
#****************************************************************************        
  def setLanguage(self,lang = None):
    #look if we have this language
    if lang != None and self.langDict.has_key(lang):
      self.langDict[lang].install();
    else: # install default language
      gettext.install('OpenRTS');

