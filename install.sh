#!/bin/bash

#-> Make sure no other pi with the same name is on the network
HOSTNAME=pi42
PASSWORD=none
CUR_USER=$(whoami)

#-> Make sure we don't run as root
if (( EUID == 0 )); then
	echo 'Please run without sudo!' 1>&2
	exit 1
fi

#-> Add common aliases
cat > $HOME/.bash_aliases <<EOF
alias sudo='sudo '
alias ll='ls -lhA'
alias ..='cd ..'
alias df='df -H'
alias du='du -ch'
alias read_cpu_temperature='/opt/vc/bin/vcgencmd measure_temp'
EOF

#-> Set passwords 'none' to current user and root user
echo -ne "$PASSWORD\n$PASSWORD\n" | sudo passwd $CUR_USER
echo -ne "$PASSWORD\n$PASSWORD\n" | sudo passwd root

#-> Set raspbian configs to match our hardware requirements
sudo sh -c 'cat >> /boot/config.txt <<EOF
max_usb_current=1
pi3-disable-bt
dtparam=audio=off
hdmi_force_hotplug=1
EOF'

#-> Update packags and install git, python and pip
sudo apt update
sudo apt install -y git python3 python3-pip python3-dev

#-> Update pip and install ipython and pyalsaaudio for audio control
sudo -H pip3 install --upgrade pip
sudo -H pip3 install --upgrade ipython

#-> Install pil and pygame, requires apt 'dev' packages
# sudo apt install -y libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev python3-numpy
# sudo -H pip3 install --upgrade Pillow pygame

#-> Install fswebcam and opencv
sudo apt install fswebcam python3-opencv

#-> Create custom autostart
AUTOSTART_CONF=$HOME/.config/lxsession/LXDE-pi/autostart
mkdir -p $(dirname $AUTOSTART_CONF)
cat > $AUTOSTART_CONF <<EOF
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
#@xscreensaver -no-splash
#@point-rpi
@/home/pi/Public/polarized_camera/run.sh
EOF

#-> Install samba server for sharing 'Public' dir via network
sudo DEBIAN_FRONTEND=noninteractive apt install -y samba samba-common-bin
echo -ne '\n\n' | sudo smbpasswd -a $CUR_USER
sudo sh -c "cat >> /etc/samba/smb.conf <<EOF
force user = $CUR_USER
wins support = yes
[Public]
 comment = PiShare
 path = $HOME/Public
 browseable = Yes
 writeable = Yes
 guest ok = yes
 public = yes
 read only = no
 force user = $CUR_USER
EOF"

#-> Remove "Welcome to Raspberry Pi" startup wizard
sudo rm /etc/xdg/autostart/piwiz.desktop

#-> Move taskbar to bottom
PANEL_CONF=$HOME/.config/lxpanel/LXDE-pi/panels/panel
mkdir -p $(dirname $PANEL_CONF)
cp /etc/xdg/lxpanel/LXDE-pi/panels/panel $PANEL_CONF
sed -i -e '/edge/s/=.*/=bottom/' $PANEL_CONF

#-> Set black wallpaper
DESKTOP_CONF=$HOME/.config/pcmanfm/LXDE-pi/desktop-items-0.conf
mkdir -p $(dirname $DESKTOP_CONF)
cat > $DESKTOP_CONF <<EOF
[*]
desktop_bg=#000000000000
wallpaper_mode=color
show_trash=0
EOF

#-> Enable ssh, expand file system, set hostname and timezone
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_hostname $HOSTNAME
sudo raspi-config nonint do_change_timezone Israel

#-> Reboot host for changes to take effect
echo 'Rebooting in 5 seconds...'
sleep 5; sudo reboot
