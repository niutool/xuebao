# -*- coding: utf-8 -*-
import datetime
from client import plugin

digit_map_high = [u"零", u"十", u"二十", u"三十", u"四十", u"五十"]
digit_map_low = u"零一二三四五六七八九十"

class ClockPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return [u"几点", u"几点钟", u"时间"]

    def _get_chinese_time(self, now):
        hh = now.hour / 10
        hl = now.hour % 10
        
        t = u""
        if hh > 0:
            t += digit_map_high[hh]
            if hl > 0:
                t += digit_map_low[hl]
        else:
            t += digit_map_low[hl]
        t += u"点"
        
        mh = now.minute / 10
        ml = now.minute % 10
        if now.minute == 0:
            t += u"整"
        else:
            t += digit_map_high[mh]
            if ml > 0:
                t += digit_map_low[ml]
            t += u"分"
        
        return t

    def handle(self, text, mic):
        """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """

        now = datetime.datetime.now()
        fmt = u"现在是北京时间" + self._get_chinese_time(now)
        mic.say(fmt)

    def get_priority(self):
        return 20

    def is_valid(self, text):
        """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() in text.lower() for p in self.get_phrases())
