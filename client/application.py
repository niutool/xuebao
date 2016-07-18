"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import logging

from client import settings, pluginstore, audioengine
from client import brain, mic, mic_mock, conversation
from client import configreader

class Xuebao(object):
    def __init__(self, use_local_mic=False):
        self._logger = logging.getLogger(__name__)
        
        # Read config
        configfile = settings.config('config.info')
        self._logger.debug("Trying to read config file: '%s'", configfile)
        
        self.config = configreader.ConfigReader()
        self.config.read(configfile)
        
        audio_engine_slug = self.config.get('Audio', 'Engine', 'alsa')
        self._logger.debug("Using Audio engine '%s'", audio_engine_slug)
        
        active_stt_slug = self.config.get('STT', 'ActiveEngine', 'sphinx')
        self._logger.debug("Using STT engine '%s'", active_stt_slug)
        
        passive_stt_slug = self.config.get('STT', 'PassiveEngine', active_stt_slug)
        self._logger.debug("Using passive STT engine '%s'", passive_stt_slug)
        
        tts_slug = self.config.get('TTS', 'Engine', 'espeak-tts')
        self._logger.debug("Using TTS engine '%s'", tts_slug)
        
        player_slug = self.config.get('Mp3Player', 'Engine', 'pygame-player')
        self._logger.debug("Using Mp3 player '%s'", player_slug)
        
        # Load plugins
        plugin_directories = [settings.PLUGIN_PATH]
        self.plugins = pluginstore.PluginStore(plugin_directories)
        self.plugins.detect_plugins()

        # Initialize AudioEngine
        ae_info = self.plugins.get_plugin(audio_engine_slug,
                                          category='audioengine')
        self.audio = ae_info.plugin_class(ae_info, self.config)

        # Initialize audio input device
        device_slug = self.config.get('Audio', 'InputDevice', None)
        try:
            if device_slug:
                input_device = self.audio.get_device_by_slug(device_slug)
            else:
                input_device = self.audio.get_default_device(False)
            
            if audioengine.DEVICE_TYPE_INPUT not in input_device.types:
                raise audioengine.UnsupportedFormat(
                    "Audio device with slug '%s' is not an input device"
                    % input_device.slug)
        except (audioengine.DeviceException) as e:
            devices = [device.slug for device in
                       self.audio.get_devices(device_type=audioengine.DEVICE_TYPE_INPUT)]
            self._logger.critical(e.args[0])
            self._logger.warning('Valid output devices: %s',
                                 ', '.join(devices))
            raise

        # Initialize audio output device
        device_slug = self.config.get('Audio', 'OutputDevice', None)
        try:
            if device_slug:
                output_device = self.audio.get_device_by_slug(device_slug)
            else:
                output_device = self.audio.get_default_device(True)
            
            if audioengine.DEVICE_TYPE_OUTPUT not in output_device.types:
                raise audioengine.UnsupportedFormat(
                    "Audio device with slug '%s' is not an output device"
                    % output_device.slug)
        except (audioengine.DeviceException) as e:
            devices = [device.slug for device in
                       self.audio.get_devices(device_type=audioengine.DEVICE_TYPE_OUTPUT)]
            self._logger.critical(e.args[0])
            self._logger.warning('Valid output devices: %s',
                                 ', '.join(devices))
            raise

        # Initialize Brain
        self.brain = brain.Brain(self.config)
        for info in self.plugins.get_plugins_by_category('speechhandler'):
            try:
                plugin = info.plugin_class(info, self.config)
            except Exception as e:
                self._logger.warning(
                    "Plugin '%s' skipped! (Reason: %s)", info.name,
                    e.message if hasattr(e, 'message') else 'Unknown',
                    exc_info=(
                        self._logger.getEffectiveLevel() == logging.DEBUG))
            else:
                self.brain.add_plugin(plugin)

        if len(self.brain.get_plugins()) == 0:
            msg = 'No plugins for handling speech found!'
            self._logger.error(msg)
            raise RuntimeError(msg)
        elif len(self.brain.get_all_phrases()) == 0:
            msg = 'No command phrases found!'
            self._logger.error(msg)
            raise RuntimeError(msg)

        active_stt_plugin_info = self.plugins.get_plugin(
            active_stt_slug, category='stt')
        active_stt_plugin = active_stt_plugin_info.plugin_class(
            'default', self.brain.get_plugin_phrases(), active_stt_plugin_info,
            self.config)

        if passive_stt_slug != active_stt_slug:
            passive_stt_plugin_info = self.plugins.get_plugin(
                passive_stt_slug, category='stt')
        else:
            passive_stt_plugin_info = active_stt_plugin_info

        keyword = settings.KEYWORD
        passive_stt_plugin = passive_stt_plugin_info.plugin_class(
            'keyword', self.brain.get_standard_phrases() + [keyword],
            passive_stt_plugin_info, self.config)

        tts_plugin_info = self.plugins.get_plugin(tts_slug, category='tts')
        tts_plugin = tts_plugin_info.plugin_class(tts_plugin_info, self.config)
        
        player_plugin_info = self.plugins.get_plugin(player_slug, category='mp3player')
        player_plugin = player_plugin_info.plugin_class(player_plugin_info, self.config)

        # Initialize Mic
        if use_local_mic:
            self.mic = mic_mock.Mic()
        else:
            self.mic = mic.Mic(
                input_device, output_device,
                passive_stt_plugin, active_stt_plugin,
                tts_plugin, player_plugin, self.config, keyword=keyword)

        self.conversation = conversation.Conversation(
            self.mic, self.brain, self.config)

    def list_plugins(self):
        plugins = self.plugins.get_plugins()
        len_name = max(len(info.name) for info in plugins)
        len_version = max(len(info.version) for info in plugins)
        for info in plugins:
            print("%s %s - %s" % (info.name.ljust(len_name),
                                  ("(v%s)" % info.version).ljust(len_version),
                                  info.description))

    def list_audio_devices(self):
        for device in self.audio.get_devices():
            device.print_device_info(
                verbose=(self._logger.getEffectiveLevel() == logging.DEBUG))

    def list_phrases(self):
        print settings.KEYWORD
        for phrase in self.brain.get_all_phrases():
            print phrase

    def run(self):
        self.conversation.greet()
        self.conversation.handleForever()
