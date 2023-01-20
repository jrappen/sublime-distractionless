#!/usr/bin/env python3.8
# coding: utf-8


from .distractionless import *


def plugin_loaded() -> None:

    distractionless.plugin_loaded(reload=False)


def plugin_unloaded() -> None:

    distractionless.plugin_unloaded()
