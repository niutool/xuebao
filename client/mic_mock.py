"""
please visit https://github.com/niutool/xuebao
for more detail

A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Jasper is always active listening with local_mic.
"""

class Mic:
    prev = None

    def __init__(self, *args, **kwargs):
        return

    def wait_for_keyword(self, keyword="JASPER"):
        return

    def active_listen(self, timeout=3):
        ainput = raw_input("YOU: ")
        self.prev = ainput
        return ainput

    def listen(self):
        return [self.active_listen(timeout=3)]

    def say(self, phrase, OPTIONS=None):
        print("JASPER: %s" % phrase)
