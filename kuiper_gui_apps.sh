#!/usr/bin/bash
echo 'Creating gui-screenshots/ in boot/'
cd /boot/ && echo analog | sudo -S mkdir -p gui-screenshots/
echo 'Creating gui-logs/ in boot/ and going back to original pwd...'
echo analog | sudo -S mkdir -p gui-logs/ && cd
pwd
echo "Checking screen version..."
screen --version
echo "Installing screen..."
echo analog | sudo -S apt-get install screen

CMDS="osc gnuradio-companion adi_colorimeter chromium-browser scopy"
for CMD in $CMDS
  do
    echo "Making a detached screen for $CMD..."
    if [ "$CMD" == "scopy" ]
    then
      CMD="flatpak run org.adi.Scopy"
      screen -S aaa -L -Logfile scopy.txt -dm $CMD
    else
      screen -S aaa -L -Logfile $CMD.txt -dm $CMD
    fi

    echo "Waiting for 65s..."
    sleep 65

    echo "Screenshotting..."
    if [ "$CMD" == "osc" ]
    then
      echo analog | sudo -S scrot "iio-osc_%Y-%m-%d.png" -e 'mv $f /boot/gui-screenshots/'
    elif [ "$CMD" == "flatpak run org.adi.Scopy" ]
    then
      echo analog | sudo -S scrot "scopy_%Y-%m-%d.png" -e 'mv $f /boot/gui-screenshots/'
    else
      echo analog | sudo -S scrot "${CMD}_%Y-%m-%d.png" -e 'mv $f /boot/gui-screenshots/' -u
    fi

    sleep 2
    echo "Kill detached screen..."
    screen -X -S aaa kill

    if [ "$CMD" == "flatpak run org.adi.Scopy" ]
    then
      echo "Moving scopy.txt to /boot/gui-logs..."
      echo analog | sudo -S cp scopy.txt /boot/gui-logs/ && cd
      rm -rf scopy.txt && cd
    else
      echo "Moving ${CMD}.txt to /boot/gui-logs..."
      echo analog | sudo -S cp $CMD.txt /boot/gui-logs/ && cd
      rm -rf ${CMD}.txt && cd
    fi

    echo "Done!"
    sleep 2
  done