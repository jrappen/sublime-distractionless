#!/usr/bin/env python
# coding: utf-8


from .src import *


def plugin_loaded():

    from .src.distractionless import _start
    _start()


def plugin_unloaded():

    from .src.distractionless import _stop
    _stop()
