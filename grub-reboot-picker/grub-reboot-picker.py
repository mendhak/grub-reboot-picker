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
    GRUB_CONFIG_PATH = "/boot/grub/grub.cfg"

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

    processing_submenu = False
    submenu_item_added = False

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
                submenu_item.connect('activate', do_grub_reboot, grub_child, grub_entry)
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

# Returns the correct version of the given command, depending on whether
# molly-guard is installed.
def molly_command(command):
    molly_command = "/sbin/{}.no-molly-guard".format(command)
    if os.path.exists(molly_command):
        return molly_command
    else:
        # Maybe this should return "/sbin/command"
        return command

def do_grub_reboot(menuitem, grub_entry, parent_grub_entry=None):
    if parent_grub_entry is not None:
        grub_reboot_value = "{}>{}".format(parent_grub_entry, grub_entry)
    else:
        grub_reboot_value = "{}".format(grub_entry)

    reboot_command = molly_command("reboot")

    if DEVELOPMENT_MODE:
        print("pkexec grub-reboot '{}' && sleep 1 && pkexec {}".format(grub_reboot_value, reboot_command))
    if not DEVELOPMENT_MODE:
        os.system("pkexec grub-reboot '{}' && sleep 1 && pkexec {}".format(grub_reboot_value, reboot_command))

def do_shutdown(_):
    shutdown_command = molly_command("shutdown")

    if DEVELOPMENT_MODE:
        print("sleep 1 && pkexec {} -h now".format(shutdown_command))
    if not DEVELOPMENT_MODE:
        os.system("sleep 1 && pkexec {} -h now".format(shutdown_command))


def quit(_):
    Gtk.main_quit()


indicator = AppIndicator3.Indicator.new(
    "customtray", icon_name,
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_menu(build_menu())


Gtk.main()
