#!/usr/bin/env bash

sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-key 0xB01FA116
apt-get update

/vagrant/install-ffmpeg.sh

apt-get install -y libgl1-mesa-dev-lts-utopic

apt-get install -y ros-jade-desktop-full
rosdep init
rosdep update

echo "source /opt/ros/jade/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo -u vagrant echo "source /opt/ros/jade/setup.bash" >> /home/vagrant/.profile

apt-get install -y python-rosinstall

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# Project dependencies
apt-get install -y gfortran libxslt1-dev libxml2-dev libxslt-dev python-devRemoved

pip install requests lxml

# Add default rules for 1394
echo "KERNEL==\"raw1394\", GROUP=\"video\"" > /etc/udev/rules.d/raw1394.rules

# Needed for Analyzer.py script
pip install rect

# Rosserial (To make communication between arduino board and ros)
apt-get install ros-indigo-rosserial-arduino
apt-get install ros-indigo-rosserial
