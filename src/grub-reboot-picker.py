#!/usr/bin/env python3
import gi
import os
import re
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3


SHOW_GRUB_MENU_SUB_MENUS = True
DEVELOPMENT_MODE = False
GRUB_CONFIG_PATH = "/boot/grub/grub.cfg"
if DEVELOPMENT_MODE:
    GRUB_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),  "grub.test3.cfg")

icon_name = "un-reboot"

def get_all_grub_entries(file_path, include_submenus=True):
    """
    Build a dictionary of Grub menu items with sub menu items if applicable. 
    Simply if it has child items it's a 'submenu' else it's just a top level menu. 
    {
        'Ubuntu': [], 
        'Advanced options for Ubuntu': [
            'Ubuntu, with Linux 6.8.0-39-generic', 
            'Ubuntu, with Linux 6.8.0-39-generic (recovery mode)'
        ], 
        'Memory test (memtest86+x64.bin)': [], 
        'Memory test (memtest86+x64.bin, serial console)': [], 
        'UEFI Firmware Settings': []
    }
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    menu_pattern = re.compile("^\\s*menuentry ['\"]([^'\"]*)['\"]")
    submenu_pattern = re.compile("^\\s*submenu ['\"]([^']*)['\"]")
    closing_brace_pattern = re.compile("^\\s*}")
    
    menu_entries = {}

    processing_submenu=False
    submenu_item_added=False
    
    for line in lines:
        submenu_match = submenu_pattern.match(line)
        menu_match = menu_pattern.match(line)
        closing_brace_match = closing_brace_pattern.match(line)
        
        if submenu_match:
            submenu_title = submenu_match.group(1)
            menu_entries[submenu_title] = []
            processing_submenu = True
        elif menu_match:
            menu_title = menu_match.group(1)
            if processing_submenu:
                menu_entries[submenu_title].append(menu_title)
                submenu_item_added = True
            else:
                menu_entries[menu_title] = []
        elif closing_brace_match:
            # submenu_item_added would match for the first nested closing brace, 
            # then processing_submenu for the top level closing brace. 
            if submenu_item_added:
                submenu_item_added = False
            elif processing_submenu:
                processing_submenu = False

    if not include_submenus:
        for k, v in list(menu_entries.items()):
            if len(v) > 0:
                del menu_entries[k]
            
    return menu_entries

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
    pattern = re.compile("^menuentry ['\"]([^'\"]*)['\"]")
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

    with open(GRUB_CONFIG_PATH, 'r') as file:
        lines = file.readlines()



    menu_pattern = re.compile("^\\s*menuentry ['\"]([^'\"]*)['\"]")
    submenu_pattern = re.compile("^\\s*submenu '([^']*)'")
    submenu_entry_pattern = re.compile("^\\s+menuentry '([^']*)'")
    # closing_brace_pattern = re.compile("^\s*\}")

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

    grub_entries = get_all_grub_entries(GRUB_CONFIG_PATH, SHOW_GRUB_MENU_SUB_MENUS)

    print(grub_entries)

    for grub_entry, grub_children in grub_entries.items():
        menuitem = Gtk.MenuItem(label=grub_entry)
        if len(grub_children) == 0:
            menuitem.connect('activate', do_grub_reboot, grub_entry)
        else:
            submenu = Gtk.Menu()
            for grub_child in grub_children:
                submenu_item = Gtk.MenuItem(label=grub_child)
                submenu_item.connect('activate', do_grub_reboot, grub_child,
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
        grub_reboot_value = "{}>{}".format(parent_grub_entry, grub_entry)
    else:
        grub_reboot_value = "{}".format(grub_entry)

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
