# -*- coding: utf-8 -*-
import os
import random
from client import plugin

class JokePlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(JokePlugin, self).__init__(*args, **kwargs)

        self._get_jokes()

    def _get_jokes(self):
        self._jokes = []
        data_path = self.profile.get("Resource", "Path", None)
        if not data_path:
            return
        
        data_path = os.path.expanduser(data_path)
        filename = os.path.join(data_path, 'joke', 'joke.txt')
        if not os.path.isfile(filename):
            return
        
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self._jokes.append(line)
    
    def get_phrases(self):
        return [u"笑话", u"幽默"]

    def handle(self, text, mic):
        if not self._jokes:
            mic.say_option('nojoke')
        else:
            joke = random.choice(self._jokes)
            mic.say(joke)

    def get_priority(self):
        return 20
    
    def is_valid(self, text):
        return any(p.lower() in text.lower() for p in self.get_phrases())
