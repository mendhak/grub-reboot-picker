#!/usr/bin/env python3
import gi
import os
import re
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3


SHOW_GRUB_MENU_SUB_MENUS = False
DEVELOPMENT_MODE = True
GRUB_CONFIG_PATH = "/boot/grub/grub.cfg"
if DEVELOPMENT_MODE:
    GRUB_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),  "grub.cfg")

icon_name = "un-reboot"


def get_grub_entries():
    """
    Builds JSON from grub menu entries, just the top level ones, like this:
    {
        "menuitems": [
            {
                "name": "Ubuntu"
            },
            {
                "name": "Windows Boot Manager (on /dev/nvme0n1p2)"
            },
            {
                "name": "UEFI Firmware Settings"
            }
        ]
    }
    """
    pattern = re.compile("^menuentry '([^']*)'")
    grub_entries = {}
    grub_entries.clear()
    grub_entries['menuitems'] = []

    for i, line in enumerate(open(GRUB_CONFIG_PATH)):
        for match in re.finditer(pattern, line):
            grub_entry = {}
            grub_entry['name'] = match.group(1)
            grub_entries['menuitems'].append(grub_entry)
            # grub_entries.append(match.group(1))
    return grub_entries


def get_grub_entries_with_submenus():
    """
    Builds JSON from grub menu entries, with sub menu items like this:
    {
        "menuitems": [
            {
                "name": "Ubuntu",
                "submenuitems": [
                    {
                        "name": "Ubuntu, with Linux 5.4.0-31-generic"
                    },
                    {
                        "name": "Ubuntu, with Linux 5.4.0-31-generic (recovery mode)"
                    },
                    {
                        "name": "Ubuntu, with Linux 5.4.0-29-generic"
                    },
                    {
                        "name": "Ubuntu, with Linux 5.4.0-29-generic (recovery mode)"
                    }
                ]
            },
            {
                "name": "Windows Boot Manager (on /dev/nvme0n1p2)",
                "submenuitems": []
            },
            {
                "name": "UEFI Firmware Settings",
                "submenuitems": []
            }
        ]
    }

    """
    menu_pattern = re.compile("^menuentry '([^']*)'")
    submenu_pattern = re.compile("^submenu '([^']*)'")
    submenu_entry_pattern = re.compile("^\\s+menuentry '([^']*)'")

    grub_entries = {}
    grub_entries.clear()
    grub_entries['menuitems'] = []
    menu_entry_match = None
    current_submenu = None
    submenu_entry_match = None

    for i, line in enumerate(open(GRUB_CONFIG_PATH)):
        menu_entry_match = re.match(menu_pattern, line)
        if menu_entry_match:
            grub_entry = {}
            grub_entry['name'] = menu_entry_match.group(1)
            grub_entries['menuitems'].append(grub_entry)
            continue

        submenu_entry_match = re.match(submenu_pattern, line)
        if submenu_entry_match:
            grub_entry = {}
            grub_entry['name'] = submenu_entry_match.group(1)
            grub_entries['menuitems'].append(grub_entry)
            # print(submenu_entry_match.group(1))
            current_submenu = grub_entry
            current_submenu['submenuitems'] = []
            continue

        if current_submenu:
            submenu_entry_match = re.match(submenu_entry_pattern, line)
            if submenu_entry_match:
                # print(submenu_entry_match.group(1))
                grub_entry = {}
                grub_entry['name'] = submenu_entry_match.group(1)
                current_submenu['submenuitems'].append(grub_entry)
    return grub_entries


def build_menu():
    menu = Gtk.Menu()

    if SHOW_GRUB_MENU_SUB_MENUS:
        grub_entries = get_grub_entries_with_submenus()
    else:
        grub_entries = get_grub_entries()
    print(grub_entries)

    for grub_entry in grub_entries['menuitems']:
        menuitem = Gtk.MenuItem(label=grub_entry['name'])
        if len(grub_entry.get('submenuitems', [])) == 0:
            menuitem.connect('activate', do_grub_reboot, grub_entry)
        else:
            submenu = Gtk.Menu()
            for grub_entry_submenuitem in grub_entry.get('submenuitems', []):
                # print(grub_entry_submenuitem)
                submenu_item = Gtk.MenuItem(label=grub_entry_submenuitem['name'])
                submenu_item.connect('activate', do_grub_reboot, grub_entry_submenuitem,
                                    grub_entry)
                submenu.append(submenu_item)
            menuitem.set_submenu(submenu)

        menu.append(menuitem)

    shutdown_item = Gtk.MenuItem(label='Shutdown')
    shutdown_item.connect('activate', do_shutdown)
    menu.append(shutdown_item)

    exittray = Gtk.MenuItem(label='Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)

    menu.show_all()
    return menu


def do_grub_reboot(menuitem, grub_entry, parent_grub_entry=None):
    if parent_grub_entry is not None:
        grub_reboot_value = "{}>{}".format(parent_grub_entry['name'], grub_entry['name'])
    else:
        grub_reboot_value = "{}".format(grub_entry['name'])

    if DEVELOPMENT_MODE:
        print("pkexec grub-reboot '{}' && sleep 1 && pkexec reboot".format(grub_reboot_value))
    if not DEVELOPMENT_MODE:
        os.system("pkexec grub-reboot '{}' && sleep 1 && pkexec reboot".format(grub_reboot_value))


def do_shutdown(_):
    if DEVELOPMENT_MODE:
        print("sleep 1 && pkexec shutdown -h now")
    if not DEVELOPMENT_MODE:
        os.system("sleep 1 && pkexec shutdown -h now")


def quit(_):
    Gtk.main_quit()

# win = Gtk.Window()
# win.connect("destroy", Gtk.main_quit)
# #win.set_icon_from_file("logo.svg")
# win.set_icon_name(icon_name)
# win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

# grid = Gtk.Grid()
# win.add(grid)

# button = Gtk.Button(label="Message")
# button.connect("clicked", on_button_clicked)
# button.set_size_request(300,100)
# #win.add(button)
# grid.add(button)

# label = Gtk.Label()
# label.set_label("Hello World")
# label.set_angle(25)
# label.set_halign(Gtk.Align.END)
# grid.attach(label, 1, 2, 2, 1)
# # win.add(label)

# statusicon = Gtk.StatusIcon()
# statusicon.set_from_file("logo.svg")
# statusicon.set_visible(True)
# statusicon.set_has_tooltip(True)

# indicator = AppIndicator3.Indicator.new("customtray",
#               os.path.abspath("logo.svg"),
#               AppIndicator3.IndicatorCategory.APPLICATION_STATUS)


indicator = AppIndicator3.Indicator.new(
    "customtray", icon_name,
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_menu(build_menu())


# def reset_menu():
#     indicator.set_menu(build_menu())
#     return True


# GLib.timeout_add(5000, reset_menu)

# win.set_default_size(500,500)
# win.show_all()

Gtk.main()
