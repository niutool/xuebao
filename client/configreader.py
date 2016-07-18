"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import logging
import ConfigParser as configparser

class ConfigReader(object):
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._logger = logging.getLogger(__name__)
    
    def read(self, filenames):
        self._config.read(filenames)
    
    def get(self, section, option, default):
        try:
            val = self._config.get(section, option)
        except configparser.NoOptionError:
            val = default
            self._logger.info("option %s not specified in profile, using defaults %s." % (option, default))
        
        return val
    
    def getint(self, section, option, default):
        try:
            val = self._config.getint(section, option)
        except configparser.NoOptionError:
            val = default
            self._logger.info("option %s not specified in profile, using defaults %d." % (option, default))
        
        return val
