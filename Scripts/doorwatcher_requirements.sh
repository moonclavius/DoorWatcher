#!/bin/bash

RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m'


echo -e ${RED}"================================${GREEN}[1/7]: Remove and Clean...${RED}================================"${NC}
sudo apt-get -y purge wolfram-engine
sudo apt-get -y purge libreoffice*
sudo apt-get -y clean
sudo apt-get -y autoremove
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[2/7]: Update System...${RED}================================"${NC}
sudo apt-get -y update
sudo apt-get -y upgrade
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[3/7]: Install OS libraries...${RED}================================"${NC}
sudo apt-get -y install build-essential cmake unzip pkg-config
sudo apt-get -y install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev

sudo apt-get -y install libgtk-3-dev
sudo apt-get -y install libcanberra-gtk*

sudo apt-get -y install libatlas-base-dev gfortran
sudo apt-get -y install python3-dev
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[4/7]: Install Python libraries...${RED}================================"${NC}
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[5/7]: Download OpenCV and OpenCV_Contrib...${RED}================================"${NC}
cd ~
sudo wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
sudo wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip

sudo unzip opencv.zip
sudo unzip opencv_contrib.zip

mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[6/7]: Install Virtual-Environment...${RED}================================"${NC}
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip

echo -e "\n# Virtualenv and Virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

source ~/.profile
mkvirtualenv cv -p python3
workon cv
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[7/7]: Install Camera modules...${RED}================================"${NC}
sudo pip3 install imutils
sudo pip3 install flask
echo "================================================================================================================================"

source ~/.profile
sudo apt autoremove
sudo apt autoclean
echo -e ${GREEN}FINISHED${NC}
echo "================================================================================================================================"
