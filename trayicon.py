#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_file("logo.svg")
        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("popup_menu", self.on_secondary_click)


    def on_secondary_click(self, widget, button, time):
        menu = Gtk.Menu()

        menu_item1 = Gtk.MenuItem("First Entry")
        menu.append(menu_item1)

        menu_item2 = Gtk.MenuItem("Quit")
        menu.append(menu_item2)
        menu_item2.connect("activate", Gtk.main_quit)

        menu.show_all()
        menu.popup(None, None, None, self, 3, time)

if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()