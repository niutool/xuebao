"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import abc
import tempfile
import wave
import mad
from client import audioengine

class GenericPlugin(object):
    def __init__(self, info, config):
        self._plugin_config = config
        self._plugin_info = info
    
    @property
    def profile(self):
        # FIXME: Remove this in favor of something better
        return self._plugin_config
    
    @property
    def info(self):
        return self._plugin_info

class AudioEnginePlugin(GenericPlugin, audioengine.AudioEngine):
    pass

class MP3PlayerPlugin(GenericPlugin):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)
    
    @abc.abstractmethod
    def load_folder(self, folder):
        pass
    
    @abc.abstractmethod
    def play(self):
        pass
    
    @abc.abstractmethod
    def stop(self):
        pass
    
    @abc.abstractmethod
    def pause(self):
        pass
    
    @abc.abstractmethod
    def resume(self):
        pass
    
    @abc.abstractmethod
    def play_next(self):
        pass
    
    @abc.abstractmethod
    def play_prev(self):
        pass

class SpeechHandlerPlugin(GenericPlugin):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)
    
    @abc.abstractmethod
    def get_phrases(self):
        pass
    
    @abc.abstractmethod
    def handle(self, text, mic):
        pass
    
    @abc.abstractmethod
    def is_valid(self, text):
        pass
    
    def get_priority(self):
        return 0

class STTPlugin(GenericPlugin):
    def __init__(self, name, phrases, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)
        self._vocabulary_phrases = phrases
        self._vocabulary_name = name
        self._vocabulary_compiled = False
        self._vocabulary_path = None
    
    @property
    def vocabulary_path(self):
        return self._vocabulary_path
    
    @classmethod
    @abc.abstractmethod
    def is_available(cls):
        return True
    
    @abc.abstractmethod
    def transcribe(self, fp):
        pass

class TTSPlugin(GenericPlugin):
    """
    Generic parent class for all speakers
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def say(self, phrase, *args):
        pass
    
    def mp3_to_wave(self, filename):
        mf = mad.MadFile(filename)
        with tempfile.SpooledTemporaryFile() as f:
            wav = wave.open(f, mode='wb')
            wav.setframerate(mf.samplerate())
            wav.setnchannels(1 if mf.mode() == mad.MODE_SINGLE_CHANNEL else 2)
            # 4L is the sample width of 32 bit audio
            wav.setsampwidth(4)
            frame = mf.read()
            while frame is not None:
                wav.writeframes(frame)
                frame = mf.read()
            wav.close()
            f.seek(0)
            data = f.read()
        return data
