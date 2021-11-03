# All tests concerning opening and closing programs,
# choosing devices, and adding devices
import os
import pyautogui
import pytest
import subprocess
import time
from test.common import locate_and_click_image


@pytest.fixture(scope="session")
def directory():
    return dir == "C:\\Users\\hrosete\\Downloads\\Analog Devices\\Scopy\\Scopy.exe"


@pytest.fixture(scope="session")
def open_program_windows(dir):
    """open_program_windows: Opens a program in Windows OS from directory.

    parameters:
        dir: type=path
            Absolute/relative path to the application's executable
    """
    try:
        os.startfile(str(dir))
    except Exception as e:
        print(str(e))
        assert False, "Kindly install the latest release of the program/application."
    time.sleep(5)


@pytest.fixture(scope="session")
def open_program_linux(app):
    """open_program_linux: Opens a program in Linux or Mac OS.

    global variable:
        PID: type=string
            The application's process ID
    parameters:
        app: type=string
            The application name that you want to stop
    """
    try:
        global PID
        subprocess.run(f"{app} &", shell=True, check=True)
        a = subprocess.run("echo $!", shell=True, capture_output=True)
        PID = a.stdout.decode()  # Call as common.PID or PID
    except Exception as e:
        print(str(e))
        assert False, f"Kindly install the latest release of {app}."
    time.sleep(5)


@pytest.fixture
def close_program_windows(app):
    """close_program_windows: Closes a program in Windows OS.

    parameters:
        app: type=string
            The application name and its extension that you want to stop
            Example: Scopy.exe
    """
    try:
        os.system(f"TASKKILL /F /IM {app}")
    except Exception as e:
        print(str(e))


@pytest.fixture
def close_program_linux(pid):
    """close_program_linux: Closes a program in Linux and Mac OS on CLI.

    parameters:
        pid: type=string
            The process ID of the application you want to stop
    """
    try:
        subprocess.run(f"kill -15 {pid}", shell=True, check=True)
        time.sleep(1)
        subprocess.run(f"kill -9 {pid}", shell=True, check=True)
    except Exception as e:
        print(str(e))


@pytest.fixture
def choose_device(device, connection="usb"):
    """choose_device: Chooses a device to connect to.

    parameters:
        device: type=string
            The device that you want to connect to
            Options are: m2k
        connection: type=string
            Connection of the device with regards to your machine.
            Options are: usb, ip, demo
    """
    if device.lower() == "m2k":
        img = os.path.join(image_path, "m2k.png")
    # elif device.lower() == "pluto":
    #     img = os.path.join(image_path, "pluto.png")

    x, y = 0, 0
    coords = pyautogui.locateAllOnScreen(img, confidence=0.95)
    for c in coords:
        l, t, w, h = c
        s1 = screenshot_region_and_save(
            screenshots_path, l, (t + h), w, 30, filename="s1.png")
        ui_text = read_text_from_image(s1, threshold=90)
        if connection.lower() == "demo":
            if "ip:127.0.0.1" in ui_text:
                x, y = pyautogui.center(c)
                break
            else:
                continue
        elif connection.lower() == "ip":
            if "ip:192" in ui_text:
                x, y = pyautogui.center(c)
                break
            else:
                continue
        elif connection.lower() == "usb":
            if connection in ui_text:
                x, y = pyautogui.center(c)
                break
            else:
                continue
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def add_device(ip="", confidence_level=0.95):
    """add_device: Add device through IP

    parameter:
        ip: type=string
            IP of the device to be connected
        confidence_level: type=int
            A scale that determines how accurate the image in the UI must be
            from that of the reference image
    """
    add_device_img = os.path.join(image_path, "add_device.png")
    locate_and_click_image(add_device_img, confidence_level)
    if ip:
        pyautogui.moveRel(0, 155, 0.5, pyautogui.easeOutQuad)
        pyautogui.click()
        pyautogui.PAUSE
        pyautogui.write(ip, interval=0.1)
        time.sleep(2)


@pytest.fixture
def popup_dialog_box(cmd="close"):
    """popup_dialog_box: Interacts with the Automatic Update Dialog box in Scopy
    parameter:
        cmd: type=string
            Interaction needed for the dialog box.
            Options: yes, no, close
    """
    update_popup_img = os.path.join(image_path, "auto_update_popup.png")
    locate_and_click_image(update_popup_img)

    if cmd.lower() == "yes":
        yes_img = os.path.join(image_path, "yes.png")
        locate_and_click_image(yes_img)
    elif cmd.lower() == "no":
        no_img = os.path.join(image_path, "no.png")
        locate_and_click_image(no_img)
    elif cmd.lower() == "close":
        close_img = os.path.join(image_path, "close.png")
        locate_and_click_image(close_img)
    time.sleep(3)
