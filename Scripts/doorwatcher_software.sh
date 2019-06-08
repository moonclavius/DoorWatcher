#!/bin/bash

RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m'


echo -e ${RED}"================================${GREEN}[1/3]: Change CONF_SWAPSIZE & install libraries...${RED}================================"${NC}
source ~/.profile
mkvirtualenv cv -p python3
workon cv

sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
sudo pip install numpy dlib
deactivate
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[2/3]: Compile and install OpenCV with OpenCV_Contrib modules...${RED}================================"${NC}
workon cv

cd opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

make -j1
make install
sudo ldconfig

sudo sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
echo "sudo modprobe bcm2835-v4l2" >> ~/.profile

source ~/.profile
echo "================================================================================================================================"


echo -e ${RED}"================================${GREEN}[3/3]: Move cv2.so...${RED}================================"${NC}
cd ~/opencv/build/lib/python3
sudo cp cv2.cpython-35m-arm-linux-gnueabihf.so /usr/local/lib/python3.5/dist-packages/cv2.so
cd ~
echo "================================================================================================================================"


sudo apt autoremove
sudo apt autoclean
echo -e ${GREEN}FINISHED${NC}
echo "================================================================================================================================"
