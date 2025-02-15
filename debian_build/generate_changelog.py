import os
import re
from datetime import datetime


suite = os.environ['suite']


def parse_changelog():
    with open('../CHANGELOG.md', 'r') as f:
        content = f.read()

    # Parse entries like "* 0.0.1: Description" followed by indented details
    entries = re.findall(r'\* ([0-9.]+):([^*]+(?:\n\s+[^*][^\n]+)*)', content)

    # Sort entries in reverse order (newest first)
    entries.sort(key=lambda x: x[0], reverse=True)

    changelog_entries = []
    timestamp = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

    for version_num, description in entries:
        desc_lines = description.strip().split('\n')
        formatted_lines = []
        for line in desc_lines:
            line = line.strip()
            if not line.startswith('*'):
                line = f'* {line}'
            formatted_lines.append(line)
        formatted_desc = '\n  '.join(formatted_lines)

        entry = f"""grub-reboot-picker ({version_num}+{suite}) {suite}; urgency=low

  {formatted_desc}

 -- Mendhak <mendhak@users.noreply.github.com>  {timestamp}"""
        changelog_entries.append(entry)

    # Join entries with single newline
    changelog = '\n\n'.join(changelog_entries) + '\n'
    return changelog


if __name__ == "__main__":
    with open('debian/changelog', 'w') as f:
        print(parse_changelog())
        f.write(parse_changelog())
