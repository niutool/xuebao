# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import logging

class Conversation(object):
    def __init__(self, mic, brain, profile):
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.profile = profile
        self.brain = brain
        self.translations = {

        }
        #  self.notifier = Notifier(profile)

    def greet(self):
        self.mic.say_option('welcome')

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.debug('Starting to handle conversation.')
        while True:
            # Print notifications until empty
            """notifications = self.notifier.get_all_notifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))"""

            ainput = self.mic.listen()

            if ainput:
                plugin, text = self.brain.query(ainput)
                if plugin and text:
                    try:
                        plugin.handle(text, self.mic)
                    except Exception:
                        self._logger.error('Failed to execute module',
                                           exc_info=True)
                        self.mic.say_option('exception')
                    else:
                        self._logger.debug("Handling of phrase '%s' by " +
                                           "module '%s' completed", text,
                                           plugin.info.name)
            else:
                self.mic.say_option('pardon')
