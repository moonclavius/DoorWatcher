# DoorWatcher
DoorWatcher is an IoT project that opens doors with the help of "face recognition". In addition it also allows monitoring via the browser. With the help of OpenCV a face can easly be recognised and identificated. Depending on the use, additional GPIO pins can be controlled to open a door, for example. 

Note: you can find all documentations for every scripes at [Documentation](/Documentation) directory.

This project is made with the help of [HackerShackOfficial](https://github.com/HackerShackOfficial/Smart-Security-Camera) and [face_recognition](https://github.com/ageitgey/face_recognition).

## Contents
* [Prerequisites](#Prerequisites)
* [Installation](#Installation)
* [Usage](#Usage)
* [Customization](#Customization)
* [Troubleshooting](#Troubleshooting)

***

## Prerequisites
### Hardware
- Raspberry Pi Zero W
- Camera V2.1 NoIR
### Software
- OpenCV & Dlib
- virtual environment
- face_recognition


## Installation
### Setup
First we will remove unnecessary packages and then we will install all required libraries with the help of the **doorwatcher_requiments.sh** script... (the installation and updating process depends on your internet speed)
  1. give the script wirting rights `chmod +x doorwatcher_requiments.sh` and run the script `sudo /.doorwatcher_requiments.sh`
### Installing Requirements
Next we are going to install all needed packages, OpenCV4, dlib, and more with the **doorwatcher_software.sh** script... (the installation process will last around 2-3h)
  1. move the script to home directory `mv ~/DoorWatcher/Scripts/doorwatcher_software.sh ~/doorwatcher_software.sh`
  2. give the script wirting rights `chmod +x doorwatcher_software.sh` and run the script `sudo /.doorwatcher_software.sh`

## Usage
1. In order for us to work with facial recognition we need to enable the interface on the Raspberry Pi. We do this with the following command: `sudo raspi-config`. Select `Interface Options`, then `Pi Camera` and toggle on. Press `Finish` and exit.

2. Run the program `sudo python3 ~/DoorWatcher/Modules/main.py`. 

You can view a live stream by visiting the ip address of your pi in a browser on the same network. You can find the ip address of your Raspberry Pi by typing `ifconfig` in the terminal and looking for the `inet` address.

Visit `<raspberrypi_ip>:5000` in your browser to view the stream.

Note: To view the live stream on a different network than your Raspberry Pi, you can use [ngrok](https://ngrok.com/) to expose a local tunnel. Once downloaded, run ngrok with `./ngrok http 5000` and visit one of the generated links in your browser.

Note: The video stream will not start automatically on startup. To start the video stream automatically, you will need to run the program from your `/etc/rc.local` file see this [video](https://www.youtube.com/watch?v=51dg2MsYHns&feature=youtu.be&t=7m4s) for more information about how to configure that.

## Customization
Frist you can change the pictures with this command `raspistill -o ~/DoorWatcher/Modules/pictures/p1.jpg` and add how much you need.

If you want to change the size of the streaming than you will need to change the file **~/DoorWatcher/Modules/templates/index.html**.
Make sure you choose the right sizes when you change the 6 line `<img id="bg" src="{{ url_for('video_feed') }}" style="height:600px; width:800px;">`.

To change the recognition time just change the line 35 `if (time.time() - last_epoch) > <TIME>:` in the file **~/DoorWatcher/Modules/main.py**.

## Troubleshooting
#### [1] ERROR
  ```
  modprobe: ERROR: ../libkmod/libkmod.c:586 kmod_search_moddep() could not open moddep file '/lib/modules/4.14.98-v7+/modules.dep.bin'
  modprobe: FATAL: Module bcm2835-v4l2 not found in directory /lib/modules/4.14.98-v7+
  modprobe: ERROR: ../libkmod/libkmod.c:586 kmod_search_moddep() could not open moddep file '/lib/modules/4.14.98-v7+/modules.dep.bin'
  modprobe: FATAL: Module bcm2835-v4l2 not found in directory /lib/modules/4.14.98-v7+
  ```
  To fix this error just simple run following command `sudo rpi-update 963a31330613a38e160dc98b708c662dd32631d5` and then reboot the     raspberry pi

#### [2] ERROR
  ```
  opencv_test_core_pch_dephelp.dir/opencv_test_core_pch_dephelp.cxx.o
  In file included from /home/joey/opencv/opencv/opencv/modules/core/test/test_precomp.hpp:12:0,
                   from /home/joey/opencv/opencv/build/modules/core/opencv_test_core_pch_dephelp.cxx:1:
  /home/joey/opencv/opencv/opencv/modules/core/include/opencv2/core/private.hpp:66:12: fatal error: Eigen/Core: No such file or directory
  #  include <Eigen/Core>
              ^~~~~~~~~~~~
  compilation terminated.
  modules/core/CMakeFiles/opencv_test_core_pch_dephelp.dir/build.make:62: recipe for target       'modules/core/CMakeFiles/opencv_test_core_pch_dephelp.dir/opencv_test_core_pch_dephelp.cxx.o' failed
  make[2]: *** [modules/core/CMakeFiles/opencv_test_core_pch_dephelp.dir/opencv_test_core_pch_dephelp.cxx.o] Error 1
  CMakeFiles/Makefile2:1229: recipe for target 'modules/core/CMakeFiles/opencv_test_core_pch_dephelp.dir/all' failed
  make[1]: *** [modules/core/CMakeFiles/opencv_test_core_pch_dephelp.dir/all] Error 2
  make[1]: *** Waiting for unfinished jobs....
  ```
  To fix this error you will need to make changes in the **cmake/OpenCVFindLibsPerf.cmake** file. If you can't find the file just go to the root directory `cd /` and run the this command `sudo find -name "OpenCVFindLibsPerf.cmake"`
  
  LINE | OLD | NEW 
  --- | --- | ---
  44 | `find_package(Eigen3 QUIET)` | `find_package(Eigen3 3.0.0)`
  49 |`list(APPEND OPENCV_LINKER_LIBS Eigen3::Eigen)`|`#list(APPEND OPENCV_LINKER_LIBS Eigen3::Eigen)`           
  50 |`set(HAVE_EIGEN 1)`| `#set(HAVE_EIGEN 1)`
  
  #### [3] ERROR
  ```
  .sh file: /bin/bash^M: bad interpreter
  ```
  To fix this error just simple run following command `sed -i -e 's/\r$//' doorwatcher_software.sh` and then agian `sudo /.doorwatcher_software.sh`
