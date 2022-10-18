#!/usr/bin/bash

# Make a gui-screenshots/ folder in boot/ if it doesn't exist
cd /boot/ && echo analog | sudo -S mkdir -p gui-screenshots/

screen --version
echo analog | sudo -S apt-get install screen
screen -S iio-osc -L -Logfile osc.txt -dm osc
sleep 10
scrot 'iio-oscilloscope_%Y-%m-%d.png' -e 'mv $f /boot/gui-screenshots/'
sleep 2
screen -X -S iio-osc kill
sleep 2
screen -S gnu -L -Logfile gnu-radio.txt -dm gnuradio-companion
sleep 45
scrot 'gnuradio_%Y-%m-%d.png' -e 'mv $f /boot/gui-screenshots/'
sleep 2
screen -X -S gnu kill
sleep 2
screen -S colorimeter -L -Logfile colorimeter.txt -dm adi_colorimeter
sleep 10
scrot 'adi-colorimeter_%Y-%m-%d.png' -e 'mv $f /boot/gui-screenshots/'
sleep 2
screen -X -S colorimeter kill
sleep 2
screen -S browser -L -Logfile browser.txt -dm chromium-browser
sleep 20
scrot 'browser_%Y-%m-%d.png' -e 'mv $f /boot/gui-screenshots/'
sleep 2
screen -X -S browser kill
sleep 2
CMD='flatpak run org.adi.Scopy'
screen -S scopy -L -Logfile scopy.txt -dm $CMD
sleep 10
scrot 'scopy_%Y-%m-%d.png' -e 'mv $f /boot/gui-screenshots/'
sleep 2
screen -X -S scopy kill
sleep 2
