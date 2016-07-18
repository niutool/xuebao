"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import os
import re
import time
import logging
import threading
import pygame
from client import plugin

FADE_MILLS = 1500

class PygamePlayerPlugin(plugin.MP3PlayerPlugin):
    def __init__(self, *args, **kwargs):
        super(PygamePlayerPlugin, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        
        pygame.mixer.init()
        
        self._index = 0
        self._volume = 20
        self._filenames = []
        self._is_playing = False
        
        self._resource_path = os.path.expanduser(self.profile.get("Resource", "Path", None))
        self._logger.debug("resource path is %s" % self._resource_path)
        if not self._resource_path or not os.path.exists(self._resource_path):
            raise Exception("invalid resource path")
    
    def load_folder(self, folder):
        self._filenames = []
        if self._is_playing:
            self.stop()
        
        self._folder = os.path.join(self._resource_path, folder)
        if not os.path.exists(self._folder):
            raise Exception("invalid mp3 folder")
        
        for f in os.listdir(self._folder):
            if re.search(".(mp3|wav)$", f) != None:
                self._filenames.append(f)
        
        self._index_file = os.path.join(self._folder, '.index')
        self._index = self._get_index()
        
        return len(self._filenames)
    
    @property
    def is_playing(self):
        return self._is_playing
    
    def _get_index(self):
        if not os.path.isfile(self._index_file):
            return 0
        
        with open(self._index_file, 'r') as f:
            i = f.read()
            if not i.strip():
                return 0
            
            return int(i)
    
    def _set_index(self, index):
        with open(self._index_file, 'w') as f:
            f.write(str(index))
    
    def _increase_index(self):
        self._index = (self._index + 1) % len(self._filenames)
        self._set_index(self._index)
    
    def _decrease_index(self):
        self._index = (self._index - 1) % len(self._filenames)
        self._set_index(self._index)
    
    def _wait_end(self):
        while self._is_playing:
            if pygame.mixer.music.get_busy() == False:
                self._put_new_music()
                continue
            
            time.sleep(0.1)
        
        self._logger.debug("quit thread while loop.")
    
    def _put_new_music(self):
        self._logger.debug("music end, add new one")
        
        self._increase_index()
        curFile = self._filenames[self._index]
        pygame.mixer.music.load(os.path.join(self._folder, curFile))
        pygame.mixer.music.play(0)
        self.set_volumn(self._volume)
    
    def set_volumn(self, volumn):
        pygame.mixer.music.set_volume(volumn)
    
    def play(self):
        if not pygame.mixer.get_init():
            return
        
        if not self._filenames:
            return
        
        curFile = self._filenames[self._index]
        self._logger.debug("play file %s" % curFile)
        pygame.mixer.music.load(os.path.join(self._folder, curFile))
        pygame.mixer.music.play(0)
        self.set_volumn(self._volume)
        
        self._is_playing = True
        self.t = threading.Thread(target=self._wait_end)
        self.t.daemon = True
        self.t.start()
    
    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.fadeout(FADE_MILLS)
        
        self._logger.debug("stop player")
        self._is_playing = False
        self.t.join()
    
    def pause(self):
        self._logger.debug("pause player")
        pygame.mixer.music.pause()
    
    def resume(self):
        self._logger.debug("resume player")
        pygame.mixer.music.unpause()
    
    def play_next(self):
        self._logger.debug("play next mp3")
        self.stop()
        self._increase_index()
        self.play()
    
    def play_prev(self):
        self._logger.debug("play prev mp3")
        self.stop()
        self._decrease_index()
        self.play()
