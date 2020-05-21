import re
pattern = re.compile("menuentry '([^']*)'")

grub_entries = []
grub_entries.clear()

for i, line in enumerate(open('/boot/grub/grub.cfg')):
    for match in re.finditer(pattern, line):
        grub_entries.append(match.group(1))


print(grub_entries)