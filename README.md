
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0











TODO:

Run:
python test.py



Build an executable: 
pyinstaller -F -w --clean  test.py


TODO
Center it on the screen
Icon for this application
Run in system tray
System tray application
Right click menu for gnome
Create executable
Create deb:
https://stackoverflow.com/questions/17401381/debianzing-a-python-program-to-get-a-deb
https://github.com/cpbotha/stdeb-minimal-example

Create deb another way:
https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable

Create deb, also: 
http://dbalakirev.github.io/2015/08/21/deb-pkg/


create folder structure, then

dpkg-deb --build helloworld_0.0.4