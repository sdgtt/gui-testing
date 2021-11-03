from test.common import *
from test.menu_test import *
from test.connect_test import *
import os
import pyautogui

image_path = os.path.join(os.getcwd(), "scopy_images")
popup_update_img = os.path.join(image_path, "auto_update_popup.png")


def main():
    pyautogui.FAILSAFE = False

    # Open Scopy; If OS is Windows, edit directory in 'path'
    path = "C:\\Users\\hrosete\\Downloads\\Analog Devices\\Scopy\\Scopy.exe"
    open_program_windows(path)
    # open_program_linux("scopy")
    # scopy_pid = PID

    popup = pyautogui.locateCenterOnScreen(popup_update_img, confidence=0.8)
    if popup:
        popup_dialog_box(cmd="close")

    # Local/USB Connection
    choose_device("m2k", "usb")
    identify()
    connect(duration=18)
    calibrate()

    # IP Connection
    add_device(ip="192.168.2.1")
    connect(duration=2)
    add()
    identify()
    connect(duration=18)
    calibrate()
    forget_device()

    # Demo
    add_device()
    enable_demo()
    connect(duration=2)
    add()
    connect(duration=10)
    forget_device()
    add_device()
    disable_demo()

    # Close Scopy
    close_program_windows("Scopy.exe")
    # close_program_linux(scopy_pid)


if __name__ == "__main__":
    main()
