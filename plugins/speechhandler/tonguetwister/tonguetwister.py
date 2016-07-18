# -*- coding: utf-8 -*-
import os
import random
from client import plugin

class TongueTwisterPlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(TongueTwisterPlugin, self).__init__(*args, **kwargs)

        self._get_tt()

    def _get_tt(self):
        self._tt = []
        data_path = self.profile.get("Resource", "Path", None)
        if not data_path:
            return
        
        data_path = os.path.expanduser(data_path)
        filename = os.path.join(data_path, 'tonguetwister', 'tonguetwister.txt')
        if not os.path.isfile(filename):
            return
        
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self._tt.append(line)
    
    def get_phrases(self):
        return [u"绕口令"]

    def handle(self, text, mic):
        if not self._tt:
            mic.say_option('notonguetwister')
        else:
            joke = random.choice(self._tt)
            mic.say(joke)

    def get_priority(self):
        return 20
    
    def is_valid(self, text):
        return any(p.lower() in text.lower() for p in self.get_phrases())
