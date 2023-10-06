import os
import pytest
import pyautogui
import time
from test.common import (
    image_path,
    screenshots_path,
    compare_images,
    screenshot_region,
    read_text_from_image,
)


#########################################
@pytest.mark.dependency()
@pytest.mark.parametrize("device", ["m2k"])
@pytest.mark.parametrize(
    "connection, ip",
    [
        ("demo", ""),
        ("ip", "192.168.2.1"),
        ("usb", ""),
    ]
)
def test_scopy_connect(
    test_popup_dialog_box,
    test_scopy_choose_device,
    device,
    connection,
    ip,
):
    test_scopy_choose_device(device, connection, ip)

    if connection.lower() == "demo":
        filename = "scopy_demo.png"
        shot_path = screenshot_region(screenshots_path, filename)
        shot_text = read_text_from_image(shot_path, 90)
        # result = compare_images()
    elif connection.lower() == "ip":
        filename = "scopy_ip.png"
        shot_path = screenshot_region(screenshots_path, filename)
        shot_text = read_text_from_image(shot_path, 90)
        # result = compare_images()
    elif connection.lower() == "usb":
        filename = "scopy_usb.png"
        shot_path = screenshot_region(screenshots_path, filename)
        shot_text = read_text_from_image(shot_path, 90)
        # result = compare_images()

    assert not "Not Responding" in shot_text
