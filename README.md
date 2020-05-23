### WIP 

App indicator, tray icon, to reboot into other grub entries.  Basically it's a wrapper around grub-reboot. Ubuntu 20.04.  

Current way of running it is 

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
./tray.py
```




### Dependencies so far

To run the script:

```
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

## Building a distributable


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







### How to run the application

```
./tray.py
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

create folder structure, then

dpkg-deb --build helloworld_0.0.4

Other references

* https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable
* http://dbalakirev.github.io/2015/08/21/deb-pkg/
* http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html

Hosting DEB on Github Pages:  
https://pmateusz.github.io/linux/2017/06/30/linux-secure-apt-repository.html