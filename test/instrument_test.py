# All common tests regarding the instruments
import os
import pytest
import pyautogui
import time
from test.common import locate_image_with_str, instruments_path

# TODO: Learn about paths from different folders from current directory
# for image_path, screenshots_path, instruments_path


@pytest.fixture
def run(instruments_path):
    """run: Run instrument"""
    run_img = os.path.join(instruments_path, "run.png")
    x, y = locate_image_with_str(run_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def run_single(instruments_path):
    """run_singe: Run the instrument for _"""
    single_img = os.path.join(instruments_path, "run_single.png")
    x, y = locate_image_with_str(single_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def stop(instruments_path):
    """stop: Stop the instrument from running"""
    stop_img = os.path.join(instruments_path, "stop.png")
    x, y = locate_image_with_str(stop_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def more_info(instruments_path):
    """more_info: more_info the instrument from running"""
    more_info_img = os.path.join(instruments_path, "more_info.png")
    x, y = locate_image_with_str(more_info_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)


@pytest.fixture
def print(instruments_path):
    """print: Print instrument's plot display"""
    print_img = os.path.join(instruments_path, "print.png")
    x, y = locate_image_with_str(print_img)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)
