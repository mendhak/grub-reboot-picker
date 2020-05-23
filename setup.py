import os
import shutil
import setuptools
from stdeb import util

util.CHANGELOG_FILE = """%(source)s (%(full_version)s) %(distname)s; urgency=low

  * source package automatically created by stdeb 0.8.5
  I added the ability to x y and z
  * Another thing changed on this date.
  I had to introduce a sleep timer for stability reasons.

 -- %(maintainer)s  %(date822)s\n"""

if not os.path.exists("tmp"):
    os.makedirs("tmp")
shutil.copy('src/grub-reboot-picker.py', 'tmp/grub-reboot-picker')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grub-reboot-picker",
    version="0.0.2",
    author="Mendhak",
    author_email="mendhak@gmail.com",
    description="Tray application, reboot into different OSes.",
    long_description="""A tray indicator application that lets you reboot
    into different OSes from its menu.
    Basically, a wrapper around grub-reboot.
    The icon sits in the tray area.
    Only tested on Ubuntu 20.04.
    """,
    long_description_content_type="text/plain",
    url="https://github.com/mendhak/grub-reboot-picker",
    packages=['src'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu 20.04",
    ],
    python_requires='>=3.6',
    install_requires=[],
    data_files=[
        ('/usr/sbin/', ['tmp/grub-reboot-picker'])
    ]
)
