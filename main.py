#!/usr/bin/env python
# coding: utf-8


from .src import *


def plugin_loaded():

    distractionless.plugin_loaded(reload=False)


def plugin_unloaded():

    distractionless.plugin_unloaded()
