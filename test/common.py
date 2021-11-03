import os
import time
import pyautogui
import pytesseract
import cv2
import pytest

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# adi_path = os.path.join(os.path.dirname(os.getcwd()), "adi")


@pytest.fixture
def image_path():
    image_path = os.path.join(os.path.dirname(
        os.getcwd()), "adi", "scopy_images")
    return image_path


@pytest.fixture
def screenshots_path():
    screenshots_path = os.path.join(
        os.path.dirname(os.getcwd()), "adi", "screenshots")
    return screenshots_path


@pytest.fixture
def instruments_path(image_path):
    instruments_path = os.path.join(image_path, "instruments")
    return instruments_path


@pytest.fixture
def screenshot_region_and_save(dir, left=0, top=0, width=1920, height=1080, filename="screenshot.png"):
    """screenshot_region_and_save: Saves screenshot from pyautogui and returns the path,
    filename, and extension of the saved screenshot. The default values for the left, top,
    width, and height arguments are specified for 1920 by 1080 screen resolution.

    parameters:
        dir: type=path
            Path to where you want to save the screenshot
        left: type=int
            Left coordinate of the region to screenshot
        top: type=int
            Top coordinate of the region to screenshot
        width: type=int
            Width in pixels of the region to screenshot
        height: type=int
            Height in pixels of the region to screenshot
        filename: type=string
            Filename and extension for the screenshot
    return:
        file: type=path
            The path, filename,and extension of the saved screenshot
    """
    picture = pyautogui.screenshot(region=(left, top, width, height))
    file = os.path.join(dir, filename)
    picture.save(file)
    return file


@pytest.fixture
def read_text_from_image(path_to_file, threshold=50):
    """read_text_from_image: Reads text from image/screenshot and returns it

    parameter:
        path_to_file: type=path
            The path, filename,and extension of the saved screenshot
        threshold: type=int
            Threshold value in pixel
    """
    pic = cv2.imread(path_to_file)
    gray_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    x, thresh = cv2.threshold(gray_pic, threshold, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    # print("Text from file:", text)
    return text


@pytest.fixture
def locate_image_with_str(img, confidence_level=0.8):
    """locate_image_with_str: Locates the image with text in the UI, confirms it,
    and returns a tuple of the location

    parameters:
        img: type=path
            Absolute/relative path of the image
        confidence_level: type=int
            A scale that determines how accurate the image in the UI must be
            from that of the reference image
    return:
        point: type=tuple
            x and y location coordinates in the UI
    """
    # img = os.path.join(image_path, "connect.png")

    # Reference image from filename
    coord = pyautogui.locateOnScreen(img, confidence=confidence_level)
    left, top, width, height = coord
    ref_text = read_text_from_image(img, threshold=130)

    # Text, image seen on the UI
    pic = screenshot_region_and_save(
        screenshots_path, left, top, width, height)
    ui_text = read_text_from_image(pic, threshold=130)

    # Compare ref's text and text
    if ui_text == ref_text:
        point = pyautogui.center(coord)
        return point
    elif coord == None:
        assert False, "The image with text can't be found on the screen."


@pytest.fixture
def locate_and_click_image(img, confidence_level=0.8):
    """locate_and_click_image: Locates the specified image in the UI and clicks it.

    parameters:
        img: type=path
            Absolute/relative path of the image
        confidence_level: type=int
            A scale that determines how accurate the image in the UI must be
            from that of the reference image
    """
    x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence_level)
    pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(2)
