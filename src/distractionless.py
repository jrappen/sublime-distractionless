#!/usr/bin/env python
# coding: utf-8


import sublime
import sublime_plugin
from collections import defaultdict


PKG_NAME = __package__.split('.')[0]
DL_PREF = None
counters = None


def plugin_loaded(reload=False):

    try:
        global counters
        counters = defaultdict(int)
        global DL_PREF
        DL_PREF = sublime.load_settings('{}.sublime-settings'.format(PKG_NAME))
        DL_PREF.clear_on_change('reload')
        DL_PREF.add_on_change('reload', lambda: plugin_loaded(reload=True))
    except Exception as e:
        print('{}: Exception: {}'.format(PKG_NAME, e))

    if reload:
        sublime.status_message('{}: Reloaded settings on change'.format(PKG_NAME))


def plugin_unloaded():

    global DL_PREF
    DL_PREF.clear_on_change('reload')


def reset_counter(id):

    global counters
    counters[id] = 0


def increment_counter(id):

    global counters
    counters[id] += 1

    return counters[id]

def reset_view_setting(V_PREF, SYNTAX_PREF, PREF, setting, default):

    if SYNTAX_PREF is not None:
        V_PREF.set(setting, SYNTAX_PREF.get(setting, PREF.get(setting, default)))
    else:
        V_PREF.set(setting, PREF.get(setting, default))


def set_view_setting(V_PREF, DF_PREF, setting, default):

    V_PREF.set(setting, DF_PREF.get(setting, default))


class DistractionlessListener(sublime_plugin.EventListener):

    @staticmethod
    def _revert_to_normal_and_reset_count(view):
        w = view.window()
        if w is None:
            w = sublime.active_window()
        reset_counter(w.id())
        # Sublime Text > Preferences > Settings
        PREF = sublime.load_settings('Preferences.sublime-settings')
        for v in w.views():
            V_PREF = v.settings()
            if V_PREF is None:
                continue
            current_syntax = V_PREF.get('syntax').split('/')[-1].split('.')[0]
            # Sublime Text > Preferences > Settings - Syntax Specific
            SYNTAX_PREF = sublime.load_settings(current_syntax + '.sublime-settings') if current_syntax is not None else None
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'draw_centered', False)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'draw_indent_guides', True)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'draw_white_space', 'selection')
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'fold_buttons', True)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'gutter', True)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'line_numbers', True)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'rulers',[])
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'scroll_past_end', True)
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'word_wrap', 'auto')
            reset_view_setting(V_PREF, SYNTAX_PREF, PREF, 'wrap_width', 0)
        if DL_PREF.get('distractionless.toggle_sidebar', True):
            w.set_sidebar_visible(True)
        if DL_PREF.get('distractionless.toggle_minimap', True):
            w.set_minimap_visible(True)

    def on_modified_async(self, view):
        if view.settings().get('is_widget', False):
            return
        w = view.window()
        if w is None:
            w = sublime.active_window()
        count = increment_counter(w.id())
        if count is not DL_PREF.get('distractionless.toggle_after', 1):
            return
        # Sublime Text > Preferences > Settings - Distraction Free
        DF_PREF = sublime.load_settings('Distraction Free.sublime-settings')
        for v in w.views():
            V_PREF = v.settings()
            if V_PREF is None:
                continue
            set_view_setting(V_PREF, DF_PREF, 'draw_centered', True)
            set_view_setting(V_PREF, DF_PREF, 'draw_indent_guides', True)
            set_view_setting(V_PREF, DF_PREF, 'draw_white_space', 'selection')
            set_view_setting(V_PREF, DF_PREF, 'fold_buttons', True)
            set_view_setting(V_PREF, DF_PREF, 'gutter', False)
            set_view_setting(V_PREF, DF_PREF, 'line_numbers', False)
            set_view_setting(V_PREF, DF_PREF, 'rulers', [])
            set_view_setting(V_PREF, DF_PREF, 'scroll_past_end', True)
            set_view_setting(V_PREF, DF_PREF, 'word_wrap', True)
            set_view_setting(V_PREF, DF_PREF, 'wrap_width', 80)
        if DL_PREF.get('distractionless.toggle_sidebar', True):
            w.set_sidebar_visible(False)
        if DL_PREF.get('distractionless.toggle_minimap', True):
            w.set_minimap_visible(False)

    def on_activated_async(self, view):
        self._revert_to_normal_and_reset_count(view)

    def on_new_async(self, view):
        self._revert_to_normal_and_reset_count(view)

    def on_clone_async(self, view):
        self._revert_to_normal_and_reset_count(view)

    def on_load_async(self, view):
        self._revert_to_normal_and_reset_count(view)

    def on_pre_save_async(self, view):
        self._revert_to_normal_and_reset_count(view)

    def on_pre_close(self, view):
        self._revert_to_normal_and_reset_count(view)
