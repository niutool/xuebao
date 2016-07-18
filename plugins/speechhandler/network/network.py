# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import socket
from client import plugin

class NetworkPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [u"报告地址"]
    
    def _parse_ip(self, ip):
        return ip.replace(".", u"点")
    
    def handle(self, text, mic):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('baidu.com', 0))
        ip = s.getsockname()[0]
        s.close()
        
        fmt = u"当前ip是：" + self._parse_ip(ip)
        mic.say(fmt)
    
    def get_priority(self):
        return 20
    
    def is_valid(self, text):
        return any(p.lower() in text.lower() for p in self.get_phrases())
