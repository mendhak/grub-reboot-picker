#!/usr/bin/env python3
import gi
import os
import re
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
except (ValueError, ImportError):
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3


SHOW_GRUB_MENU_SUB_MENUS = True
DEVELOPMENT_MODE = os.environ.get("DEBUG", False)

icon_name = "un-reboot"


def get_all_grub_entries(include_submenus=True):
    """
    Runs grub-mkconfig and gets the grub output. 
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

    grub_mkconfig_output = subprocess.check_output(["pkexec", "grub-mkconfig"], stderr=subprocess.STDOUT)
    lines = grub_mkconfig_output.decode("utf-8").splitlines()

    menu_pattern = re.compile(r"^\s*menuentry ['\"]([^'\"]*)['\"]")
    submenu_pattern = re.compile(r"^\s*submenu ['\"]([^'\"]*)['\"]")
    closing_brace_pattern = re.compile(r"^\s*}")

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


def get_grub_entries_with_args(grub_entries):
    """
    Returns a list of Grub menu items with the arguments for grub-reboot. 
    [
        {
        "title": "Ubuntu", 
        "grub_reboot_args": "Ubuntu"
        },
        {
            "title": "Advanced options for Ubuntu",
            "children": [
                {
                "title": "Ubuntu, with Linux 6.8.0-39-generic",
                "grub_reboot_args": "Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-39-generic",
                },
                {
                "title": "Ubuntu, with Linux 6.8.0-39-generic (recovery mode)",
                "grub_reboot_args": "Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-39-generic (recovery mode)",
        },
        {
            "title": "Memory test (memtest86+x64.bin)",
            "grub_reboot_args": "Memory test (memtest86+x64.bin)",
        },
        {
            "title": "Memory test (memtest86+x64.bin, serial console)",
            "grub_reboot_args": "Memory test (memtest86+x64.bin, serial console)",
        },
        {
            "title": "UEFI Firmware Settings",
            "grub_reboot_args": "UEFI Firmware Settings",
    ]
    """

    grub_entries_with_args = []
    for title, children in grub_entries:
        if len(children) > 0:
            child_entries = []
            for child in children:
                child_entries.append({
                    "title": child,
                    "grub_reboot_args": f"{title}>{child}",
                })
            grub_entries_with_args.append({
                "title": title,
                "children": child_entries
            })
        else:
            grub_entries_with_args.append({
                "title": title,
                "grub_reboot_args": title,
            })

    return grub_entries_with_args


def build_menu():
    menu = Gtk.Menu()

    grub_entries = get_all_grub_entries(SHOW_GRUB_MENU_SUB_MENUS)
    grub_entries_with_args = get_grub_entries_with_args(grub_entries.items())

    print(grub_entries_with_args)

    menu_item_memory_test = Gtk.MenuItem(label="Memory Test")
    sub_menu_memory_test = Gtk.Menu()

    for entries in grub_entries_with_args:

        if "children" in entries and len(entries["children"]) > 0:
            menu_item = Gtk.MenuItem(label=entries["title"])
            sub_menu = Gtk.Menu()
            for child in entries["children"]:
                sub_menu_item = Gtk.MenuItem(label=child["title"])
                sub_menu_item.connect('activate', do_grub_reboot, child["grub_reboot_args"])
                sub_menu.append(sub_menu_item)
            menu_item.set_submenu(sub_menu)
            menu.append(menu_item)
        elif entries["title"].startswith("Memory test"):
            submenu_item_memory_test = Gtk.MenuItem(label=entries["title"])
            submenu_item_memory_test.connect('activate', do_grub_reboot, entries["grub_reboot_args"])
            sub_menu_memory_test.append(submenu_item_memory_test)
        else:
            menu_item = Gtk.MenuItem(label=entries["title"])
            menu_item.connect('activate', do_grub_reboot, entries["grub_reboot_args"])
            menu.append(menu_item)

    if len(sub_menu_memory_test.get_children()) > 0:
        menu_item_memory_test.set_submenu(sub_menu_memory_test)
        menu.append(menu_item_memory_test)

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


def do_grub_reboot(_, grub_reboot_args):
    reboot_command = molly_command("reboot")

    print("pkexec grub-reboot '{}' && sleep 1 && pkexec {}".format(grub_reboot_args, reboot_command))
    if not DEVELOPMENT_MODE:
        os.system("pkexec grub-reboot '{}' && sleep 1 && pkexec {}".format(grub_reboot_args, reboot_command))


def do_shutdown(_):
    shutdown_command = molly_command("shutdown")

    print("sleep 1 && pkexec {} -h now".format(shutdown_command))
    if not DEVELOPMENT_MODE:
        os.system("sleep 1 && pkexec {} -h now".format(shutdown_command))


def quit(_):
    Gtk.main_quit()


# The icon ought to get deployed to /usr/share/icons/hicolor/scalable/apps/, 
# so it can just be referenced by name. 
icon_name = "grub-reboot-picker"

# Local development
if os.path.exists("./assets/grub-reboot-picker.svg"):
    icon_name = os.path.abspath("./assets/grub-reboot-picker.svg")

indicator = AppIndicator3.Indicator.new(
    "customtray", icon_name,
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_menu(build_menu())


Gtk.main()
