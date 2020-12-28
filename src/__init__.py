#!/usr/bin/env python
# coding: utf-8


import sublime

from .distractionless import *
from .window_commands import *


PKG_NAME = __package__.split('.')[0]


def is_installed():
    pkgctrl_settings = sublime.load_settings('Package Control.sublime-settings')
    return PKG_NAME in set(pkgctrl_settings.get('installed_packages', []))


def plugin_loaded():
    distractionless.plugin_loaded()

    try:
        from package_control import events
        w = sublime.active_window()
        if events.install(PKG_NAME) and not is_installed():
            w.run_command('distractionless_open_docs', {'resource_path': '.sublime/messages/install.md'})
        elif events.post_upgrade(PKG_NAME):
            w.run_command('distractionless_open_docs', {'resource_path': '.sublime/messages/upgrade.md'})
    except Exception as e:
        print('{}: Exception: {}'.format(PKG_NAME, e))

def plugin_unloaded():
    distractionless.plugin_unloaded()
