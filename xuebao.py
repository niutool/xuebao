#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import sys
import logging
import argparse

from client import settings
from client import application

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Xuebao: the story robot')
    parser.add_argument('--local', action='store_true', help='Use text input instead of a real microphone')
    parser.add_argument('--debug', action='store_true', help='Print debug messages')
    list_info = parser.add_mutually_exclusive_group(required=False)
    list_info.add_argument('--list-plugins', action='store_true', help='List plugins and exit')
    list_info.add_argument('--list-audio-devices', action='store_true', help='List audio devices and exit')
    list_info.add_argument('--list-phrases', action='store_true', help='List phrases and exit')
    args = parser.parse_args()
    
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=settings.LOG_FILE,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info('=' * 64)
    logging.info('-%s-' % 'XUEBAO - The Story Robot'.center(62))
    logging.info('-%s-' % '(c) 2015 niutool.com'.center(62))
    logging.info('=' * 64)
    
    app = application.Xuebao(use_local_mic=args.local)
    if args.list_plugins:
        app.list_plugins()
        sys.exit(1)
    
    elif args.list_audio_devices:
        app.list_audio_devices()
        sys.exit(0)
    
    elif args.list_phrases:
        app.list_phrases()
        sys.exit(2)
    
    app.run()
