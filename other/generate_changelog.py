import os
import re
import sys
from datetime import datetime


suite = os.environ['suite']

def parse_entries_from_changelog(changelog_file_name):
    with open('CHANGELOG.md', 'r') as f:
        content = f.read()

    entries = re.findall(
        r'\* ([0-9.]+) \(([^)]+)\):([^*]+(?:\n\s+[^*][^\n]+)*)', content)
    
    return entries

def print_latest_changelog_entry():
    entries = parse_entries_from_changelog('CHANGELOG.md')
    # print(entries[-1][2].split('\n')[0].strip('*').strip().join('\n'))
    final = ""
    lines = entries[-1][2].split('\n')
    for line in lines:
        if line.startswith('*'):
            final += line.strip('*').strip() + '\n'
        else:
            final += line.strip() + '\n'
    print(final)

def generate_debian_changelog():

    entries = parse_entries_from_changelog('CHANGELOG.md')
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

    if len(sys.argv) > 1 and sys.argv[1] == 'print-latest-changelog-entry':
        print_latest_changelog_entry()
        sys.exit(0)
    else:
        suite = os.environ['suite']
        with open('debian/changelog', 'w') as f:
            f.write(generate_debian_changelog())
