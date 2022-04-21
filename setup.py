import os
import shutil
import setuptools
from stdeb import util

# Spacing is *critical* in the entire changelog file string.
with open("CHANGELOG.md", "r") as fh:
    changelog = fh.read()

util.CHANGELOG_FILE = """%(source)s (%(full_version)s) %(distname)s; urgency=low

{}

 -- %(maintainer)s  %(date822)s\n""".format(changelog)

if not os.path.exists("tmp"):
    os.makedirs("tmp")
shutil.copy('src/grub-reboot-picker.py', 'tmp/grub-reboot-picker')


setuptools.setup(
    name="grub-reboot-picker",
    version=os.getenv('version', '0.0.1'),
    author="Mendhak",
    author_email="mendhak@users.noreply.github.com",
    description="Tray application, reboot into different OSes.",
    long_description="""This tray indicator application lets you reboot
    into different OSes based on the grub menu.
    Basically, a wrapper around grub-reboot command.
    The icon sits in the tray area in gnome.
    Only tested on Ubuntu 20.04, 22.04.
    """,
    long_description_content_type="text/plain",
    url="https://github.com/mendhak/grub-reboot-picker",
    packages=['src'],
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu 22.04",
    ],
    python_requires='>=3.6',
    install_requires=[],
    data_files=[
        ('/usr/sbin/', ['tmp/grub-reboot-picker']),
        ('/usr/share/polkit-1/actions/', ['com.mendhak.grubrebootpicker.policy']),
        ('/etc/xdg/autostart/', ['com.mendhak.grubrebootpicker.desktop']),
        ('/usr/share/applications/', ['com.mendhak.grubrebootpicker.desktop'])
    ]
)
