"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import os
import requests
import tempfile
from client import plugin

class BaiduNetworkError(Exception):
    pass

class BaiduParamError(Exception):
    pass

class BaiduPhraseError(Exception):
    pass

class BaiduTTSPlugin(plugin.TTSPlugin):
    def __init__(self, *args, **kwargs):
        plugin.TTSPlugin.__init__(self, *args, **kwargs)
        
        self._app_key = self.profile.get("BaiduTTS", "AppKey", None)
        if not self._app_key:
            raise BaiduParamError("empty baidu app key")
        self._secret_key = self.profile.get("BaiduTTS", "SecretKey", None)
        if not self._secret_key:
            raise BaiduParamError("empty baidu secret key")
        self._language = self.profile.get("BaiduTTS", "Language", "zh")
        self._timeout = self.profile.getint("BaiduTTS", "Timeout", 2)
        
        self._spd = self.profile.getint("BaiduTTS", "SPD", 5)
        self._pit = self.profile.getint("BaiduTTS", "PIT", 5)
        self._vol = self.profile.getint("BaiduTTS", "VOL", 5)
        self._per = self.profile.getint("BaiduTTS", "PER", 0)
        
        self._token = None
    
    def get_token(self, app_key, secret_key, timeout):
        data = {'grant_type': 'client_credentials', 'client_id': app_key, 'client_secret': secret_key}
        r = requests.post("https://openapi.baidu.com/oauth/2.0/token", data=data, timeout=timeout)
        r.raise_for_status()
        
        return r.json()['access_token']
    
    def say(self, phrase):
        if len(phrase) > 1024:
            raise BaiduPhraseError("Text length must less than 1024 bytes")
        
        if not self._token:
            self._token = self.get_token(self._app_key, self._secret_key, self._timeout)
        
        url = "http://tsn.baidu.com/text2audio"
        data = {"tex": phrase, "lan": self._language, "tok": self._token,
                "ctp": 1, "cuid": '93489083242',
                "spd": self._spd, "pit": self._pit, "vol": self._vol, "per": self._per,}
        r = requests.post(url, data=data, timeout=self._timeout, stream=True)
        r.raise_for_status()
        content_type = r.headers['content-type']
        if content_type.startswith('application/json'):
            json_result = r.json()
            raise BaiduNetworkError("%d - %s" % (json_result['err_no'], json_result['err_msg']))
        elif content_type.startswith('audio/mp3'):
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fd:
                for chunk in r.iter_content(1024):
                    fd.write(chunk)
                tmpfile = fd.name
            data = self.mp3_to_wave(tmpfile)
            os.remove(tmpfile)
            return data
