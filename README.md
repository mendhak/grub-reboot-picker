# Grub Reboot Picker  [![CI](https://github.com/mendhak/grub-reboot-picker/workflows/CI/badge.svg)](https://github.com/mendhak/grub-reboot-picker/actions)

This utility is an app indicator (tray icon) to help you reboot into other OSes, or UEFI/BIOS, or the same OS.  
Instead of picking the OS you want during reboot at the grub menu, you can just preselect it from the menu here.  
Basically it's a wrapper around `grub-reboot`.  

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


## TODO

Configuration file or Configuration screen: 
* Top level or double level menu items
* Nicknames for menu items  

StartupNotify = true might be causing 'wait' cursor to appear

Run a single instance of the application



## Running it locally from this repo


You can run this application directly from this git repo.  

First get the dependencies

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

Clone this repo, then run the python script. 

```
cd grub-reboot-picker
sudo ./grub-reboot-picker.py
```

You'll get prompted because the script wants to run `grub-mkconfig` which generates the grub config output. 
Alternatively run the script with sudo so that you don't get prompted.  

### Running it with molly-guard

molly-guard is a package that prompts you before reboot/shutdown, preventing accidental reboots. 
This script will run the .no-molly-guard version of reboot/shutdown to bypass molly-guard.  

To test it locally, need to install molly-guard then add two environment variables to /etc/environment. 

```
sudo apt install molly-guard
echo "ALWAYS_QUERY_HOSTNAME=1" | sudo tee -a /etc/environment
echo "PRETEND_SSH=1" | sudo tee -a /etc/environment
```

Then run the script as before

```
cd grub-reboot-picker
sudo ./grub-reboot-picker.py
```


## Building a distributable

This project uses pybuild to create a .deb file. The pyproject.toml file holds the information needed to do the build, and there are additional configuration files in debian folder such as control, links, install, changelog. All of these get used by pybuild to create the .deb.  

The `debian` directory contains the files needed to build the .deb, but the .deb appears in the parent directory for some reason. It's messy which is why I prefer the Docker way. 


### Build using Docker

```
# Set the version and suite (noble, jammy, etc)
nano version.sh
# Update the changelog, carefully
nano CHANGELOG.md

# Read the version
source version.sh

# Build the image which will build the deb
docker build --build-arg version=$version --build-arg suite=$suite --progress=plain -t docker-deb-builder .
# Alternately: docker buildx bake deb-builder

# Now grab the deb and dsc files
mkdir -p output
cd output
docker create --name docker-deb-builder docker-deb-builder
docker cp docker-deb-builder:/build/grub-reboot-picker_${version}.dsc ./
docker cp docker-deb-builder:/build/grub-reboot-picker_${version}.tar.xz ./
docker cp docker-deb-builder:/build/grub-reboot-picker_${version}_all.deb ./
docker rm docker-deb-builder
ls -lah 
```

### Build on a local machine

First, some build dependencies:

```
sudo apt install dpkg-dev fakeroot debhelper python3-all dh-python lintian devscripts python3-hatchling pybuild-plugin-pyproject build-essential
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

# Generate and test changelog
python3 other/generate_changelog.py
dpkg-parsechangelog -l debian/changelog

# Build the package
dpkg-buildpackage -uc -us

# Grab the deb and dsc files
mkdir -p output; mv ../grub-reboot-picker_${version}* output/

```

## Inspecting the deb

Either way, once the .deb is built, it's good to inspect it.  

```
cd output

# Run a lint against this deb, check for errors
lintian grub-reboot-picker_${version}_all.deb

# Look at information about this deb
dpkg -I grub-reboot-picker_${version}_all.deb

# List all the files in the deb
dpkg -c grub-reboot-picker_${version}_all.deb

# Extract contents to a dir
dpkg-deb -R grub-reboot-picker_${version}_all.deb extracted/

# View changelog
zless extracted/usr/share/doc/grub-reboot-picker/changelog.gz
rm -rf extracted/

# View its dependencies
dpkg-deb -f grub-reboot-picker_${version}_all.deb Depends
```


## Uploading to Launchpad


After building, to upload to launchpad, I have to extract the sources, then GPG sign, then use dput to push up.  
Then wait for launchpad to build the code, which can take up to an hour. 

```
cd output
# Extract the source into a subdirectory
dpkg-source -x grub-reboot-picker_${version}.dsc
cd grub-reboot-picker-${version}/
# Build a debian package and GPG sign it - it uses the key id from the changelog
debuild -S -sa
# Also possible to specify the key id: debuild -S -sa -k6989CF77490369CFFDCBCD8995E7D75C76CBE9A9
# Upload to launchpad
dput ppa:mendhak/ppa ../grub-reboot-picker_${version}_source.changes
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
