#!/usr/bin/env python3.8
# coding: utf-8


from __future__ import annotations                                              # https://docs.python.org/3.8/library/__future__.html

import sublime                                                                  # EXECUTABLE_DIR/Lib/python38/sublime.py
import sublime_plugin                                                           # EXECUTABLE_DIR/Lib/python38/sublime_plugin.py


from collections import defaultdict                                             # https://docs.python.org/3.8/library/collections.html
import typing                                                                   # https://docs.python.org/3.8/library/typing.html

if typing.TYPE_CHECKING:
    import sublime_types                                                        # EXECUTABLE_DIR/Lib/python38/sublime_types.py


PKG_NAME: typing.Final[str] = __package__.split('.')[0]
PREF: typing.Optional[sublime.Settings] = None
counters = None


def plugin_loaded(
    reload: typing.Optional[bool] = False
) -> None:

    try:
        global counters
        counters = defaultdict(int)
        global PREF
        PREF = sublime.load_settings(f'Preferences.sublime-settings')
        PREF.clear_on_change('reload')
        PREF.add_on_change('reload', lambda: plugin_loaded(reload=True))
    except Exception as e:
        print(f'{PKG_NAME}: Exception: {e}')

    if reload:
        sublime.status_message(f'{PKG_NAME}: Reloaded preferences on change.')
    else:
        sublime.status_message(f'{PKG_NAME}: Plugin loaded.')


def plugin_unloaded() -> None:

    try:
        global PREF
        if PREF is not None:
            PREF = None
        global counters
        if counters is not None:
            counters = None
    except Exception as e:
        print(f'{PKG_NAME}: Exception: {e}')

    print(f'{PKG_NAME}: Plugin unloaded.')


def reset_counter(
    id: int
) -> None:

    try:
        global counters
        if counters is not None:
            counters[id] = 0
    except Exception as e:
        print(f'{PKG_NAME}: Exception: {e}')


def increment_counter(
    id: int
) -> int:

    try:
        global counters
        if counters is not None:
            counters[id] += 1
            return counters[id]
    except Exception as e:
        print(f'{PKG_NAME}: Exception: {e}')
    return 0



class DistractionlessListener(sublime_plugin.EventListener):

    def __set_v_pref(
        self,
        V_PREF: sublime.Settings,
        DF_PREF: sublime.Settings,
        setting: str,
        default: sublime_types.Value
    ) -> None:
        V_PREF.set(setting, DF_PREF.get(setting, default))

    def __reset_v_pref(
        self,
        V_PREF: sublime.Settings,
        SYNTAX_PREF: typing.Optional[sublime.Settings],
        setting: str,
        default: sublime_types.Value
    ) -> None:
        if PREF is None:
            print(f'{PKG_NAME}: Failed to reset view settings, Preferences were not loaded.')
            return
        if SYNTAX_PREF is not None:
            V_PREF.set(setting, SYNTAX_PREF.get(setting, PREF.get(setting, default)))
        else:
            V_PREF.set(setting, PREF.get(setting, default))

    def __revert_to_normal_and_reset_count(self, view) -> None:
        if PREF is None:
            return
        w: typing.Optional[sublime.Window] = view.window()
        if w is None:
            w = sublime.active_window()
        reset_counter(w.id())
        for v in w.views():
            V_PREF: typing.Optional[sublime.Settings] = v.settings()
            if V_PREF is None:
                continue
            current_syntax: str = V_PREF.get('syntax').split('/')[-1].split('.')[0]
            # Sublime Text > Preferences > Settings - Syntax Specific
            SYNTAX_PREF: typing.Final[typing.Optional[sublime.Settings]] = sublime.load_settings(current_syntax + '.sublime-settings') if current_syntax is not None else None
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'draw_centered', False)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'draw_indent_guides', True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'draw_white_space', 'selection')
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'fold_buttons', True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'gutter', True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'line_numbers', True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'rulers',[])
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'scroll_past_end', True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'word_wrap', 'auto')
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, 'wrap_width', 0)
        if PREF.get('distractionless.toggle_sidebar', True):
            w.set_sidebar_visible(True)
        if PREF.get('distractionless.toggle_minimap', True):
            w.set_minimap_visible(True)

    def on_modified_async(self, view) -> None:
        if PREF is None:
            return
        if view.settings().get('is_widget', False):
            return
        w: typing.Optional[sublime.Window] = view.window()
        if w is None:
            w = sublime.active_window()
        count: typing.Final[int] = increment_counter(w.id())
        if count is not PREF.get('distractionless.toggle_after', 1):
            return
        # Sublime Text > Preferences > Settings - Distraction Free
        DF_PREF: typing.Final[typing.Optional[sublime.Settings]] = sublime.load_settings('Distraction Free.sublime-settings')
        for v in w.views():
            V_PREF: typing.Optional[sublime.Settings] = v.settings()
            if V_PREF is None:
                continue
            self.__set_v_pref(V_PREF, DF_PREF, 'draw_centered', True)
            self.__set_v_pref(V_PREF, DF_PREF, 'draw_indent_guides', True)
            self.__set_v_pref(V_PREF, DF_PREF, 'draw_white_space', 'selection')
            self.__set_v_pref(V_PREF, DF_PREF, 'fold_buttons', True)
            self.__set_v_pref(V_PREF, DF_PREF, 'gutter', False)
            self.__set_v_pref(V_PREF, DF_PREF, 'line_numbers', False)
            self.__set_v_pref(V_PREF, DF_PREF, 'rulers', [])
            self.__set_v_pref(V_PREF, DF_PREF, 'scroll_past_end', True)
            self.__set_v_pref(V_PREF, DF_PREF, 'word_wrap', True)
            self.__set_v_pref(V_PREF, DF_PREF, 'wrap_width', 80)
        if PREF.get('distractionless.toggle_sidebar', True):
            w.set_sidebar_visible(False)
        if PREF.get('distractionless.toggle_minimap', True):
            w.set_minimap_visible(False)

    def on_activated_async(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_new_async(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_clone_async(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_load_async(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_pre_save_async(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_pre_close(self, view) -> None:
        self.__revert_to_normal_and_reset_count(view)
