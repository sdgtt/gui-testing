# All test and fixtures for the menu
import os
import pytest
import pyautogui
import time
from test.common import locate_image_with_str, image_path

# TODO: Learn about paths from different folders from current directory
# for image_path, screenshots_path


@pytest.fixture
def connect(image_path, duration=25):
    """connect: Connect UI to the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    connect_img = os.path.join(image_path, "connect.png")
    x, y = locate_image_with_str(connect_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    print("Connecting...")
    time.sleep(duration)


@pytest.fixture
def disconnect(image_path):
    """disconnect: Donnect the chosen device to the UI"""
    disconnect_img = os.path.join(image_path, "disconnect.png")
    x, y = locate_image_with_str(disconnect_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    print("Disconnecting...")
    time.sleep(3)


@pytest.fixture
def identify(image_path, duration=5):
    """identify: Identify the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    identify_img = os.path.join(image_path, "identify.png")
    x, y = locate_image_with_str(identify_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(duration)


@pytest.fixture
def forget_device(image_path):
    """forget_device: Forget the chosen device"""
    forget_device_img = os.path.join(image_path, "forget_device.png")
    x, y = locate_image_with_str(forget_device_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(5)


@pytest.fixture
def calibrate(image_path, duration=10):
    """calibrate: Forget the chosen device

    parameter:
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    calibrate_img = os.path.join(image_path, "calibrate.png")
    x, y = locate_image_with_str(calibrate_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    print("Calibrating...")
    time.sleep(duration)


@pytest.fixture
def enable_demo(image_path):
    """enable_demo: Enable M2K demo mode"""
    enable_demo_img = os.path.join(image_path, "enable_demo.png")
    x, y = locate_image_with_str(enable_demo_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def disable_demo(image_path):
    """disable_demo: Disable M2K demo mode"""
    disable_demo_img = os.path.join(image_path, "disable_demo.png")
    x, y = locate_image_with_str(disable_demo_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def add(image_path):
    """add: Add device that is connected via IP"""
    add_img = os.path.join(image_path, "add.png")
    x, y = locate_image_with_str(add_img, confidence_level=0.8)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def register(image_path):
    """register: Register device's licence on myAnalog"""
    register_img = os.path.join(image_path, "register.png")
    x, y = locate_image_with_str(register_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)
    # Add steps for registering the device online
