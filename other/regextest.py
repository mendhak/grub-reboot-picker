import re
import json


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

    for i, line in enumerate(open('/boot/grub/grub.cfg')):
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

    for i, line in enumerate(open('/boot/grub/grub.cfg')):
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


print(json.dumps(get_grub_entries(), indent=4, sort_keys=True))
print(json.dumps(get_grub_entries_with_submenus(), indent=4, sort_keys=True))

# { "menuitems": [
#     {
#         "name": "Ubuntu",
#         "submenuitems": [
#             {"name": "Ubuntu Recovery 5.39"},
#             {"name": "Ubuntu Recovery 5.39 without graphics"}
#         ]
#     },
#     {
#         "name": "Windows"

#     },
#     {
#         "name": "UEFI"

#     }
# ]}
