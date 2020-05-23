### WIP 

App indicator, tray icon, to reboot into other grub entries.  Basically it's a wrapper around grub-reboot. Ubuntu 20.04.  

Current way of running it is 

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
cd src
./grub-reboot-picker.py
```



## Building a distributable

Using [setuptools](https://setuptools.readthedocs.io/en/latest/) with [stdeb](https://github.com/astraw/stdeb).  
This produces a source package, and then creates a `.deb` package in the `deb_dist` directory. 


```
# Clean everything
rm -rf deb_dist dist *.tar.gz *.egg* build tmp
# Create the source and deb
python3 setup.py --command-packages=stdeb.command bdist_deb
# Run a lint against this deb
lintian deb_dist/grub-reboot-picker_0.0.2-1_all.deb
# Look at information about this deb
dpkg -I deb_dist/grub-reboot-picker_0.0.2-1_all.deb
```

TODO: put the .deb somewhere! 




------

### Notes:

Hard to figure out what to do here.  So many options. 

### pyinstaller

`pyinstaller` can create a single executable.  To build a single executable: 

```
pyinstaller -F -w --clean  tray.py
```

But the [size is very large](https://github.com/pyinstaller/pyinstaller/issues/2337), about 200+MB.  

Abandoned. 

### setuptools


I could build a .deb using Python's recommended [setuptools](https://packaging.python.org/tutorials/packaging-projects/). 



References:
* https://stackoverflow.com/questions/17401381/debianzing-a-python-program-to-get-a-deb
* https://github.com/cpbotha/stdeb-minimal-example
* http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html


Dependencies needed to build: 

```
sudo apt install python3-stdeb fakeroot python-all dh-python
```





### TODOs

TODO
Center it on the screen 
Icon for this application  
Run in system tray  
System tray application  
Right click menu for gnome  
Create executable  

Run via pkexec policykit without password
https://unix.stackexchange.com/questions/203136/how-do-i-run-gui-applications-as-root-by-using-pkexec

Create deb:  
https://stackoverflow.com/questions/17401381/debianzing-a-python-program-to-get-a-deb
https://github.com/cpbotha/stdeb-minimal-example

Create deb another way:
https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable

Create deb, also: 
http://dbalakirev.github.io/2015/08/21/deb-pkg/
http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html


Creating by hand:  
https://blog.packagecloud.io/eng/2015/07/14/using-dh-make-to-prepare-debian-packages/  
https://blog.packagecloud.io/eng/2016/12/15/howto-build-debian-package-containing-simple-shell-scripts/


Other references

* https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable
* http://dbalakirev.github.io/2015/08/21/deb-pkg/
* http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html

Hosting DEB on Github Pages:  
https://pmateusz.github.io/linux/2017/06/30/linux-secure-apt-repository.html