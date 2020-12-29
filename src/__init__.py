#!/usr/bin/env python
# coding: utf-8


from .distractionless import *
from .window_commands import *


def plugin_loaded():
    distractionless.plugin_loaded()
    window_commands.plugin_loaded()

def plugin_unloaded():
    distractionless.plugin_unloaded()
    # window_commands.plugin_unloaded()
