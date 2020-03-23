# wokrking machine MacOS (Unix/\*nix)
- BOOT_VOLUME_PATH is different to Linux
# schoolPI
- automated setup of raspberrypi
## Base to GUI
- Linux-Kernel - Debian - Raspbian - XFCE - arc
## Setup I
Set up the micro sd on your computer
### Burn MicroSD
- `python sd_config.py`
-  Burn Linux Distribution (Debian -> Raspbian) on sd
## Setup II
### Linux Distribution
Debian:
- Raspbian Lite
- Packagemanager: apt-get
#### Get the latest file infos on you local computer
`sudo apt-get update`
`sudo apt-get upgrade`
### Desktop Environment
`sudo apt-get tree`
#### XFCE4
`sudo apt-get install xfce4 xfce4-terminal`
OR
`sudo apt-get install xfce4 xfce4-all`
`sudo update-alternatives --config x-session-manager`
- select the ID to boot it `On my screenshot I have changed default colors, you could do this in the Applications menu > Settings > Appearance`
`sudo apt-get install arc-theme`
`sudo apt-get install arc-icons`
# clean SD
`sudo apt-get remove lxappearance lxde lxde-* lxinput lxmenu-data lxpanel lxpolkit lxrandr lxsession* lxsession lxshortcut lxtask lxterminal
sudo apt-get install pistore
sudo apt-get autoremove
sudo apt-get autoclean
sudo reboot`
## Setup III
### Graphical Packagemanager
`sudo apt install synaptic`
### Browser
- Chromium
`sudo apt install chromium-browser`

- [ ] create personal_data.py template
    - host computer password of the burning machine
- [ ] solution for entering server with pseude terminal...
- [ ] tests


## hints
stdout=PIPE,
stderr=PIPE
if all piped the pw wont set well...
``` python
proc = Popen('sudo -S dd bs=1m if={} of={} conv=sync'
             .format(IMAGE_FILE_PATH, disk_name),
             shell=True,
             stdin=PIPE,
             # # stdout=PIPE,
             # # stderr=PIPE,
             )
proc.communicate(personal_data.pw)
```
