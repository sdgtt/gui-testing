import os
import pyautogui
import pytesseract
import time
from test.common import (
    # from common import (
    image_path,
    screenshots_path,
    prettify_move_and_click,
    read_text_from_image,
    locate_and_click_image,
    locate_image_with_str,
    screenshot_region,
)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def scopy_add_device(duration=2):
    """scopy_add_device: Clicks the 'Add' button. This adds a device to the
    list of existing connected devices.

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    add_device_img = os.path.join(image_path, "Scopy_add.png")
    locate_image_with_str(add_device_img, sleep_duration=duration)


def scopy_add_plus(ip="", confidence_lvl=0.95, duration=5):
    """scopy_add_plus: Clicks the '+' button on the GUI. It also adds a device
    that is connected via IP.

    parameter:
        ip: type=string
            IP of the device to be connected
        confidence_lvl: type=int
            A scale that determines how accurate the image in the UI must be
            from that of the reference image
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    add_plus_img = os.path.join(image_path, "Scopy_add_plus.png")
    locate_and_click_image(
        add_plus_img, sleep_duration=duration, confidence_level=confidence_lvl)
    time.sleep(5)
    if ip:
        pyautogui.moveRel(0, 155, 0.5, pyautogui.easeOutQuad)
        pyautogui.click()
        time.sleep(2)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        time.sleep(2)
        pyautogui.write(ip, interval=0.1)
        time.sleep(2)


def scopy_choose_device(device, connection="demo", ip=""):
    """scopy_choose_device: Chooses a device to connect to.

    parameters:
        device: type=string
            The device that you want to connect to
            Options are: m2k
        connection: type=string
            Connection of the device with regards to your machine.
            Options are: demo, usb, ip
        ip: type=string
            Must be used if connection is through IP.
            IP of the device to be connected
    """
    try:
        if device.lower() == "m2k":
            m2k_img = os.path.join(image_path, "Scopy_m2k.png")

            if connection.lower() == "usb" or connection.lower() == "ip":
                x, y = 0, 0
                coords = pyautogui.locateAllOnScreen(m2k_img, confidence=0.95)
                for coord in coords:
                    l, t, w, h = coord
                    s1_path = screenshot_region(
                        screenshots_path,
                        filename="m2k_device.png",
                        left=l,
                        top=(t + h),
                        width=w,
                        height=30
                    )
                    # Read text from screenshot
                    ui_text = read_text_from_image(s1_path, 40)

                    if connection.lower() == "usb":
                        if connection in ui_text:
                            x, y = pyautogui.center(coord)
                            prettify_move_and_click(x, y)
                            time.sleep(5)
                            scopy_connect(duration=20)
                            break
                    elif connection.lower() == "ip":
                        if ip:
                            if ip == ui_text:
                                x, y = pyautogui.center(coord)
                                prettify_move_and_click(x, y)
                                time.sleep(5)
                                scopy_connect(duration=20)
                                break
                            else:
                                time.sleep(5)
                                scopy_add_plus(ip)
                                scopy_connect(duration=5)
                                scopy_add_device()
                                scopy_connect(duration=15)
                                break
                        else:
                            raise Exception("An IP must be included.")
            else:
                scopy_add_plus()
                scopy_enable_demo(duration=5)
                scopy_connect(duration=5)
                scopy_add_device()
                scopy_connect(duration=15)
    except Exception as e:
        raise Exception(e)


def scopy_calibrate(duration=45):
    """scopy_calibrate: Forget the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    calibrate_img = os.path.join(image_path, "Scopy_calibrate.png")
    locate_image_with_str(calibrate_img, sleep_duration=duration)


def scopy_connect(duration=25):
    """scopy_connect: Connect UI to the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    connect_img = os.path.join(image_path, "Scopy_connect.png")
    locate_image_with_str(connect_img, sleep_duration=duration)


def scopy_disconnect(duration=5):
    """scopy_disconnect: Donnect the chosen device to the UI

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    disconnect_img = os.path.join(image_path, "Scopy_disconnect.png")
    locate_image_with_str(disconnect_img, sleep_duration=duration)


def scopy_disable_demo(duration=3):
    """scopy_disable_demo: Disable M2K demo mode

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    disable_demo_img = os.path.join(image_path, "Scopy_disable_demo.png")
    locate_image_with_str(disable_demo_img, sleep_duration=duration)


def scopy_enable_demo(duration=3):
    """scopy_enable_demo: Enable M2K demo mode

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    enable_demo_img = os.path.join(image_path, "Scopy_enable_demo.png")
    locate_image_with_str(
        enable_demo_img, sleep_duration=duration, confidence_level=0.7)


def scopy_forget_device(duration=5):
    """scopy_forget_device: Forget the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    forget_device_img = os.path.join(image_path, "Scopy_forget_device.png")
    locate_image_with_str(forget_device_img, sleep_duration=duration)


def scopy_identify(duration=5):
    """scopy_identify: Identify the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    identify_img = os.path.join(image_path, "Scopy_identify.png")
    locate_image_with_str(identify_img, sleep_duration=duration)


def scopy_register(duration=2):
    """scopy_register: Register device's licence on myAnalog

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    register_img = os.path.join(image_path, "Scopy_register.png")
    locate_image_with_str(register_img, sleep_duration=duration)
    # Add steps for registering the device online
