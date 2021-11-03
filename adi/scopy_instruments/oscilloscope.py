from test.common import locate_and_click

import os
import time
import pyautogui

image_path = os.path.join(os.getcwd(), "scopy_images")
run_img = os.path.join(image_path, "run.png")
stop_img = os.path.join(image_path, "stop.png")
single_run_img = os.path.join(image_path, "run_single.png")
print_img = os.path.join(image_path, "print.png")
en_mixed_signal_img = os.path.join(image_path, "enable_mixed_signal_view.png")
general_settings_img = os.path.join(image_path, "general_settings.png")
ch1_img = os.path.join(image_path, "ch1.png")
ch2_img = os.path.join(image_path, "ch2.png")
more_info_img = os.path.join(image_path, "more_info.png")
disable_ch1_img = os.path.join(image_path, "disable_ch1.png")
disable_ch2_img = os.path.join(image_path, "disable_ch2.png")


def main():
    # print("Current Working Directory: ", os.getcwd())
    # print("Welcome to Scopy's Oscilloscope!")

    # Disable CH1
    locate_and_click(disable_ch1_img)
    time.sleep(2)

    # Disable CH2
    locate_and_click(disable_ch2_img)
    time.sleep(2)

    # Enable CH1
    x, y = pyautogui.locateCenterOnScreen(ch1_img)
    pyautogui.doubleClick(x, y)
    time.sleep(2)

    # Enable CH2
    x, y = pyautogui.locateCenterOnScreen(ch2_img)
    pyautogui.doubleClick(x, y)
    time.sleep(2)


if __name__ == "__main__":
    main()

# class oscilloscope():
#     def __init__(self) -> None:
#         pass

#     def run(image):
#         go = pyautogui.locateCenterOnScreen(image)
#         pyautogui.click(go)
