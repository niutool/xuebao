# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

from client import plugin

class PlayerControllerPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [u"停止播放", u"暂停播放", u"继续播放", u"下一首", u"上一首", u"下一个", u"上一个"]
    
    def handle(self, text, mic):
        cmd = ""
        for t in text.lower().split():
            if t in self.get_phrases():
                cmd = t
                break
        
        if not mic.player.is_playing:
            mic.say_option('noplaying')
            return
        
        if cmd == u"停止播放":
            mic.player.stop()
        elif cmd == u"暂停播放":
            mic.player.pause()
        elif cmd == u"继续播放":
            mic.player.resume()
        elif cmd in [u"下一首", u"下一个"]:
            mic.player.play_next()
        elif cmd in [u"上一首", u"上一个"]:
            mic.player.play_prev()
    
    def is_valid(self, text):
        return any(p.lower() in text.lower() for p in self.get_phrases())

