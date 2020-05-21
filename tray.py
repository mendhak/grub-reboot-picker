#!/usr/bin/env python3

import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import re

icon_name="un-reboot"

def on_button_clicked(widget):
    print("Clicked!")

def get_grub_entries():
  pattern = re.compile("menuentry '([^']*)'")
  grub_entries = []
  grub_entries.clear()

  for i, line in enumerate(open('/boot/grub/grub.cfg')):
      for match in re.finditer(pattern, line):
          grub_entries.append(match.group(1))
  return grub_entries

def menu():
  menu = Gtk.Menu()
  
  grub_entries = get_grub_entries()

  for grub_entry in grub_entries:
    command_g = Gtk.MenuItem(label=grub_entry)
    command_g.connect('activate', note, grub_entry)
    menu.append(command_g)

  # command_one = Gtk.MenuItem(label=randomstr)
  # command_one.connect('activate', note)
  # menu.append(command_one)

  exittray = Gtk.MenuItem(label='Exit Tray')
  exittray.connect('activate', quit)
  menu.append(exittray)
  
  menu.show_all()
  return menu
  
def note(menuitem, grub_entry):
  print(grub_entry)
  os.system("pkexec grub-reboot '{}' && sleep 1 && pkexec reboot".format(grub_entry))
  #os.system("gedit $HOME/Documents/notes.txt")


def quit(_):
  Gtk.main_quit()    

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
#win.set_icon_from_file("logo.svg")
win.set_icon_name(icon_name)
win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)


grid = Gtk.Grid()
win.add(grid)


button = Gtk.Button(label="Message")
button.connect("clicked", on_button_clicked)
button.set_size_request(300,100)
#win.add(button)
grid.add(button)


label = Gtk.Label()
label.set_label("Hello World")
label.set_angle(25)
label.set_halign(Gtk.Align.END)
grid.attach(label, 1, 2, 2, 1)
# win.add(label)


# statusicon = Gtk.StatusIcon()
# statusicon.set_from_file("logo.svg")
# statusicon.set_visible(True)
# statusicon.set_has_tooltip(True)

#indicator = AppIndicator3.Indicator.new("customtray", os.path.abspath("logo.svg"), AppIndicator3.IndicatorCategory.APPLICATION_STATUS)  
indicator = AppIndicator3.Indicator.new("customtray", icon_name, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)  
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_menu(menu())

def reset_menu():
  indicator.set_menu(menu())
  return True

#GLib.timeout_add(5000, reset_menu)

win.set_default_size(500,500)
win.show_all()

print(get_grub_entries())

Gtk.main()
