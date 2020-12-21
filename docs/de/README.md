# distractionless Erweiterung für [`Sublime Text`](https://www.sublimetext.com)

> Automatisch in einen fensterbasierten, ablenkungsfreien Modus von Sublime Text beim Editieren wechseln.

* [Dokumentation](#dokumentation)
* [Voraussetzungen](#voraussetzungen)
* [Installation](#installation)
* [Verwendung](#verwendung)
* [Quellcode](#quellcode)
* [Spenden](#spenden)

## Dokumentation

> Eine plug-in Dokumentation ist über das Menü oder die Kurzbefehleingabe (command palette) verfügbar.

* Englisch (English):
  <https://github.com/jrappen/sublime-distractionless/blob/master/docs/en/README.md>
* Deutsch:
  <https://github.com/jrappen/sublime-distractionless/blob/master/docs/de/README.md>

### Code of conduct

<https://github.com/jrappen/.github/blob/master/CODE_OF_CONDUCT.md>

### Contributing guide

<https://github.com/jrappen/.github/blob/master/CONTRIBUTING.md>

## Voraussetzungen

distractionless ist als Erweiterung für die **neusten Build** von Sublime Text gedacht und erfordert im Moment **`Build 4074`** oder neuer.

* Lade [Sublime Text](https://www.sublimetext.com) herunter
* [Installiere Package Control](https://packagecontrol.io/installation) über den Menüeintrag: `Tools > Install Package Control`
    * Schließe und öffne Sublime Text nach der Installation von Package Control.

## Installation

Die Verwendung von **Package Control** wird vorausgesetzt, da es deine Erweiterungen (mit ihren Abhängigkeiten) aktuell hält.

### Installation über Package Control

* Öffne die Befehlseingabe (`Tools > Command Palette`).
* Wähle `Package Control: Install Package`.
* Suche nach [`distractionless` in Package Control](https://packagecontrol.io/packages/distractionless) und wähle die Erweiterung aus, um sie zu installieren.

## Verwendung

`distractionless` lässt Sublime Text automatisch in den [Distraction Free mode](https://www.sublimetext.com/docs/distraction_free.html) innerhalb eines normalen Fensters wechseln, sobald du beginnst, eine Datei zu bearbeiten.

`distractionless` lässt Sublime Text automatisch zurück in den normalen Modus wechseln, sobald:

* du eine Datei speicherst, öffnest oder klonst.
* einen neuen Tab öffnest, den Tab wechselst oder schließt.
* Sublime Text in den Vordergrund wechselt.

### Einstellungen

Verwende die Einstellungen von Sublime Text um anzupassen, wie Ansichten in jedem Modus dargestellt werden:

* `Preferences > Settings`
* `Preferences > Settings - Syntax Specific`
* `Preferences > Settings - Distraction Free`

Passe folgende Einstellungen an:

```jsonc
//  Packages/User/Preferences.sublime-settings

{
    "auto_hide_menu": true,
    "auto_hide_status_bar": true,
    "auto_hide_tabs": true
}
```

Verwende die `distractionless` Einstellungen um weiter anzupassen, wann und was beim Umschalten zwischen den Modi passiert:

```jsonc
//  Packages/User/Preferences.sublime-settings

{
//  Anzahl der Änderungen, nach denen die Oberfläche automatisch gewechselt wird
    "distractionless.toggle_after": 1,

//  wechsle die Anzeige der minimap beim Wechseln der Anzeige-Modi
    "distractionless.toggle_minimap": true,

//  wechsle die Anzeige der sidebar beim Wechseln der Anzeige-Modi
    "distractionless.toggle_sidebar": true
}
```

## Quellcode

<https://www.github.com/jrappen/sublime-distractionless>

### Lizenz

<https://github.com/jrappen/sublime-distractionless/blob/master/LICENSE>

### Feedback

Verwende für Feedback bitte die Befehlseingabe (command palette) oder das Menü.

## Spenden

<https://www.paypal.me/jrappen>
