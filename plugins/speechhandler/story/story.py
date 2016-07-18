# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

from client import plugin

class StoryPlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(StoryPlugin, self).__init__(*args, **kwargs)
    
    def get_phrases(self):
        return [u"故事", u"音乐", u"儿歌", u"学习", u"胎教"]
    
    def handle(self, text, mic):
        path = ""
        for t in text.lower().split():
            if t in self.get_phrases():
                path = t
                break
        
        if not path:
            mic.say_option('emptyfolder')
            return
        
        x = mic.player.load_folder(path)
        if x > 0:
            mic.say_option('ok')
            mic.player.play()
        else:
            mic.say_option('emptyfile')

    def get_priority(self):
        return 10
    
    def is_valid(self, text):
        return any(p.lower() in text.lower() for p in self.get_phrases())
