#!/bin/bash
sudo apt-get update
sudo apt-get install python3 python3-pip curl unzip firefox -yf
sudo apt install -y python3 python3-pip
sudo pip3 install --upgrade pip 
sudo pip3 install Pillow
sudo apt install -y tesseract-ocr
DEBIAN_FRONTEND=noninteractive sudo apt install -y python3-xlib
sudo apt install -y xvfb xserver-xephyr scrot
sudo apt install -y firefox-geckodriver
sudo pip3 install -r requirements_linux.txt
sudo add-apt-repository ppa:alexlarsson/flatpak
sudo apt update
sudo apt install -y flatpak
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
sudo flatpak install -y flathub org.kde.Platform//5.15
sudo flatpak install -y flathub org.kde.Sdk//5.15
wget https://github.com/analogdevicesinc/scopy/releases/download/v1.3.0/scopy-v1.3.0-Linux.flatpak.zip
unzip scopy-v1.3.0-Linux.flatpak.zip
sudo flatpak install -y Scopy.flatpak