#!/usr/bin/env python3.14
# coding: utf-8


from __future__ import annotations                                              # https://docs.python.org/3.14/library/__future__.html

import sublime                                                                  # EXECUTABLE_DIR/Lib/python314/sublime.py
import sublime_plugin                                                           # EXECUTABLE_DIR/Lib/python314/sublime_plugin.py


from collections import defaultdict                                             # https://docs.python.org/3.14/library/collections.html
import typing                                                                   # https://docs.python.org/3.14/library/typing.html

if typing.TYPE_CHECKING:
    import sublime_types                                                        # EXECUTABLE_DIR/Lib/python314/sublime_types.py


PKG_NAME: str | None = str(__package__).split(sep='.')[0]
PREF: sublime.Settings | None = None
counters = None


def plugin_loaded() -> None:

    try:
        global counters
        counters = defaultdict(int)
        global PREF
        PREF = sublime.load_settings(base_name=f'Preferences.sublime-settings')
        PREF.clear_on_change(tag='reload')
        PREF.add_on_change(tag='reload', callback=lambda: plugin_loaded())
    except Exception as e:
        print(f'{PKG_NAME}: Exception:\n\n{e}')


def plugin_unloaded() -> None:

    try:
        global PREF
        PREF = None
        global counters
        counters = None
    except Exception as e:
        print(f'{PKG_NAME}: Exception:\n\n{e}')


def reset_counter(id: int) -> None:

    try:
        global counters
        if counters is not None:
            counters[id] = 0
    except Exception as e:
        print(f'{PKG_NAME}: Exception:\n\n{e}')


def increment_counter(id: int) -> int:

    try:
        global counters
        if counters is not None:
            counters[id] += 1
            return counters[id]
    except Exception as e:
        print(f'{PKG_NAME}: Exception:\n\n{e}')
    return 0



class DistractionlessListener(sublime_plugin.EventListener):

    def __set_v_pref(
        self,
        V_PREF: sublime.Settings,
        DF_PREF: sublime.Settings,
        key: str,
        default: sublime_types.Value
    ) -> None:
        V_PREF.set(key=key, value=DF_PREF.get(key=key, default=default))

    def __reset_v_pref(
        self,
        V_PREF: sublime.Settings,
        SYNTAX_PREF: sublime.Settings | None,
        key: str,
        default: sublime_types.Value
    ) -> None:
        if PREF is None:
            print(f'{PKG_NAME}: Failed to reset view settings, Preferences were not loaded.')
            return
        if SYNTAX_PREF is not None:
            V_PREF.set(key=key, value=SYNTAX_PREF.get(key=key, default=PREF.get(key=key, default=default)))
        else:
            V_PREF.set(key=key, value=PREF.get(key=key, default=default))

    def __revert_to_normal_and_reset_count(self, view: sublime.View) -> None:
        if PREF is None:
            return
        w: sublime.Window | None = view.window()
        if w is None:
            w = sublime.active_window()
        reset_counter(id=w.id())
        for v in w.views():
            V_PREF: sublime.Settings | None = v.settings()
            if V_PREF is None:
                continue
            # syntax().name might return nothing if sublime-syntax file does not return a name field
            current_syntax: str = 'Plain text' if v.syntax() is None else v.syntax().name or v.syntax().path.split(sep='/')[-1].split(sep='.')[0]
            # Sublime Text > Preferences > Settings - Syntax Specific
            SYNTAX_PREF: sublime.Settings | None = sublime.load_settings(base_name=current_syntax + '.sublime-settings') if current_syntax is not None else None
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='draw_centered', default=False)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='draw_indent_guides', default=True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='draw_white_space', default='selection')
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='fold_buttons', default=True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='gutter', default=True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='line_numbers', default=True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='rulers', default=[])
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='scroll_past_end', default=True)
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='word_wrap', default='auto')
            self.__reset_v_pref(V_PREF, SYNTAX_PREF, key='wrap_width', default=0)
        if PREF.get(key='distractionless.toggle_sidebar', default=True):
            w.set_sidebar_visible(flag=True)
        if PREF.get(key='distractionless.toggle_minimap', default=True):
            w.set_minimap_visible(flag=True)

    def on_modified_async(self, view: sublime.View) -> None:
        if PREF is None:
            return
        if view.settings().get(key='is_widget', default=False):
            return
        w: sublime.Window | None = view.window()
        if w is None:
            w = sublime.active_window()
        count: typing.Final[int] = increment_counter(id=w.id())
        if count is not PREF.get(key='distractionless.toggle_after', default=1):
            return
        # Sublime Text > Preferences > Settings - Distraction Free
        DF_PREF: typing.Final[sublime.Settings | None] = sublime.load_settings(base_name='Distraction Free.sublime-settings')
        for v in w.views():
            V_PREF: sublime.Settings | None = v.settings()
            if V_PREF is None:
                continue
            self.__set_v_pref(V_PREF, DF_PREF, key='draw_centered', default=True)
            self.__set_v_pref(V_PREF, DF_PREF, key='draw_indent_guides', default=True)
            self.__set_v_pref(V_PREF, DF_PREF, key='draw_white_space', default='selection')
            self.__set_v_pref(V_PREF, DF_PREF, key='fold_buttons', default=True)
            self.__set_v_pref(V_PREF, DF_PREF, key='gutter', default=False)
            self.__set_v_pref(V_PREF, DF_PREF, key='line_numbers', default=False)
            self.__set_v_pref(V_PREF, DF_PREF, key='rulers', default=[])
            self.__set_v_pref(V_PREF, DF_PREF, key='scroll_past_end', default=True)
            self.__set_v_pref(V_PREF, DF_PREF, key='word_wrap', default=True)
            self.__set_v_pref(V_PREF, DF_PREF, key='wrap_width', default=80)
        if PREF.get(key='distractionless.toggle_sidebar', default=True):
            w.set_sidebar_visible(flag=False)
        if PREF.get(key='distractionless.toggle_minimap', default=True):
            w.set_minimap_visible(flag=False)

    def on_activated_async(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_new_async(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_clone_async(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_load_async(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_pre_save_async(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)

    def on_pre_close(self, view: sublime.View) -> None:
        self.__revert_to_normal_and_reset_count(view)
