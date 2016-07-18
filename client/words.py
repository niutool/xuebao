"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import random
import ConfigParser as configparser

from client import settings

class OptionError(Exception):
    pass

class Words(object):
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._parse()
    
    def _parse(self):
        configfile = settings.config('words.info')
        self._config.read(configfile)
        
        self._settings = {}
        for k, v in self._config.items('Settings'):
            self._settings[k] = v
        
        self._words = {}
        for k, v in self._config.items('Words', 0, self._settings):
            self._words[k] = v.decode('utf8').split()
    
    def get(self, option):
        tmp = self._words.get(option)
        if not tmp:
            raise OptionError("invalid option")
        
        return random.choice(tmp)
