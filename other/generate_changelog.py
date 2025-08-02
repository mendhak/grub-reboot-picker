import os
import re
from datetime import datetime


suite = os.environ['suite']


def parse_changelog():
    with open('CHANGELOG.md', 'r') as f:
        content = f.read()

    entries = re.findall(
        r'\* ([0-9.]+) \(([^)]+)\):([^*]+(?:\n\s+[^*][^\n]+)*)', content)
    
    print(entries)

    # Sort entries in reverse order (newest first, by date)
    entries.sort(key=lambda x: x[1], reverse=True)

    changelog_entries = []
    for version_num, date_str, description in entries:
        # Convert YYYY-MM-DD to debian format
        entry_date = datetime.strptime(date_str, '%Y-%m-%d')
        timestamp = entry_date.strftime('%a, %d %b %Y 00:00:00 +0000')

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

    return '\n\n'.join(changelog_entries) + '\n'


if __name__ == "__main__":
    suite = os.environ['suite']
    with open('debian/changelog', 'w') as f:
        f.write(parse_changelog())
