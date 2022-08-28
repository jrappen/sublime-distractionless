#!/usr/bin/env python
# coding: utf-8


from __future__ import annotations

from .src import *


def plugin_loaded() -> None:

    distractionless.plugin_loaded(reload=False)


def plugin_unloaded() -> None:

    distractionless.plugin_unloaded()
