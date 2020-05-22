import re
import json

menu_pattern = re.compile("^menuentry '([^']*)'")
submenu_pattern = re.compile("^\\s+menuentry '([^']*)'")

grub_entries = {}
grub_entries.clear()
grub_entries['menuitems'] = []
menu_entry_match = None
current_submenu = False
submenu_entry_match = None


for i, line in enumerate(open('/boot/grub/grub.cfg')):
    menu_entry_match = re.match(menu_pattern, line)
    if menu_entry_match:
        grub_entry = {}
        grub_entry['name'] = menu_entry_match.group(1)
        grub_entries['menuitems'].append(grub_entry)
        #print(menu_entry_match.group(1))
        current_submenu = grub_entry
        current_submenu['submenuitems'] = []
        continue

    if current_submenu:
        submenu_entry_match = re.match(submenu_pattern, line)
        if submenu_entry_match:
            #print(submenu_entry_match.group(1))
            grub_entry = {}
            grub_entry['name'] = submenu_entry_match.group(1)
            current_submenu['submenuitems'].append(grub_entry)

    #for match in re.finditer(pattern, line):
    #    grub_entries.append(match.group(1))


print(json.dumps(grub_entries, indent=4, sort_keys=True))



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