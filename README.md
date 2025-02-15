# Grub Reboot Picker  [![CI](https://github.com/mendhak/grub-reboot-picker/workflows/CI/badge.svg)](https://github.com/mendhak/grub-reboot-picker/actions)

This utility is an app indicator (tray icon) to help you reboot into other OSes, or UEFI/BIOS, or the same OS.  
Instead of picking the OS you want during reboot at the grub menu, you can just preselect it from the menu here.  
Basically it's a wrapper around `grub-reboot`. I've only tested this on Ubuntu 20.04, 22.04, 24.04. 

![screenshot](assets/screenshot.png) 

## Install it

apt install:

```
sudo add-apt-repository ppa:mendhak/ppa
sudo apt update
sudo apt install grub-reboot-picker
```


## Run it

The application will auto start the next time you log in to Ubuntu.  
You can also launch it directly by searching for `Grub Reboot Picker` in Activities


## Use it

Click on the application icon.  
A menu with grub entries will appear.  
Click one of the entries.  
After a moment, Ubuntu will reboot.  
The grub menu item you chose should be preselected. 


# TODO

Configuration file or Configuration screen: 
* Top level or double level menu items
* Nicknames for menu items  

StartupNotify = true might be causing 'wait' cursor to appear

Run a single instance of the application



# Developing locally

## Running it from this repo

You can run this application directly from this git repo.  

First get the dependencies

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1

```

Clone this repo, then run the python script. 

```
cd src
sudo ./grub-reboot-picker.py
```

Sudo is required here because grub.cfg may not be readable (0600 permission)

## Building a distributable

Using [setuptools](https://setuptools.readthedocs.io/en/latest/) with [stdeb](https://github.com/astraw/stdeb).  
This produces a source package, and then creates a `.deb` package in the `deb_dist` directory. 

First, some build dependencies:

```
sudo apt install python3-stdeb fakeroot python3-all dh-python lintian devscripts python3-hatchling pybuild-plugin-pyproject
```

Then to build:

```
# Set the version and suite (noble, jammy, etc)
nano version.sh
# Update the changelog, carefully
nano CHANGELOG.md
# Read the version
source version.sh
# Clean everything
git clean -fdx
# Create the source and deb
cd debian_build/
# Generate and test changelog
python3 generate_changelog.py
dpkg-parsechangelog -l debian/changelog
# Build the package
dpkg-buildpackage -uc -us

# Back up to the parent, for some reason the deb is created in the parent dir
cd ..

# Run a lint against this deb, check for errors
lintian grub-reboot-picker_${version}_all.deb
# Look at information about this deb
dpkg -I grub-reboot-picker_${version}_all.deb
# List all the files in the deb
dpkg -c grub-reboot-picker_*.deb
# Extract contents to a dir
dpkg-deb -R grub-reboot-picker_*.deb extracted/
# View changelog
less tmp/usr/share/doc/grub-reboot-picker/changelog.gz
# View its dependencies
dpkg-deb -f grub-reboot-picker_*.deb Depends
```

The setup.py is the starting point, which runs setuptools.  Which uses stdeb to run commands to create the .deb.  
[The `setup.cfg`](https://github.com/astraw/stdeb#stdeb-distutils-command-options) contains arguments to use for the package generation, both for setuputils as well as stdeb for things like Debian control file, changelog, etc.   
The `MANIFEST.in` includes non-code files which are still needed.  
I've modified setup.py a bit to generate Debian's changelog from the CHANGELOG.md, it's very sensitive to spacing.    


After building, to upload to launchpad, you have to extract the sources, then GPG sign, then use dput to push up.  Then wait for launchpad to build the code, which can take up to an hour. 

```
cd tmp
# Extract the source into a subdirectory
dpkg-source -x ../deb_dist/grub-reboot-picker_$version-1.dsc
cd grub-reboot-picker-$version/
# Build a debian package and GPG sign it
debuild -S -sa
# Upload to launchpad
dput ppa:mendhak/ppa ../grub-reboot-picker_$version-1_source.changes
```


## Application structure

There's a lot happening in a .deb file.  For my own benefit, here are the files it creates, and their purpose. 

![diagram](assets/diagram.drawio.svg)

### .desktop file

The `com.mendhak.grubrebootpicker.desktop` file goes in two places. 

`/etc/xdg/autostart/` -  ensures that the app is launched when the user logs in  
`/usr/share/applications/` - ensures that the app can be found when searching through Activities. 

### .policy file

The `com.mendhak.grubrebootpicker.policy` is a [polkit policy file](https://wiki.archlinux.org/index.php/Polkit) goes in `/usr/share/polkit-1/actions/`.  
This in turn allows the application to run `pkexec reboot` without a password prompt.  

### The script

As part of the build the `.py` extension is removed.  During install, the executable, extensionless Python script is put in `/usr/sbin` so that it's on the user's $PATH.  
