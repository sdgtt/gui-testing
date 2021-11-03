import os
import pyautogui
import pytesseract
import cv2
import time
from PIL import Image
from test.common import screenshot_region_and_save, read_text_from_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = os.path.join(os.getcwd(), "scopy_images")
screenshots_path = os.path.join(os.getcwd(), "screenshots")

img = os.path.join(image_path, "m2k.png")
coords = pyautogui.locateAllOnScreen(img, confidence=0.95)
for c in coords:
    l, t, w, h = c
    s1 = screenshot_region_and_save(
        screenshots_path, l, (t + h), w, h-105, filename="s1.png")
    ui_text = read_text_from_image(s1, threshold=90)
    print(ui_text)

# coord_list = []
# for c in coords:
#     # print(tuple(c))
#     coord_list.append(tuple(c))
# print(f"coord_list: {coord_list}")


# coord = pyautogui.locateCenterOnScreen(img, confidence=0.8)
# print(type(coord))
# print(coord)
# print()
# c = pyautogui.locateOnScreen(img, confidence=0.8)
# print(type(c))
# print(c)

# left, top, width, height = coord
# print(coord)

# picture = pyautogui.screenshot(region=(left, top-30, width, height-105))
# picture.save(os.path.join(screenshots_path, "screenshot_1.png"))
# pic = cv2.imread(os.path.join(screenshots_path, "screenshot_1.png"))
# gray_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
# x, thresh = cv2.threshold(gray_pic, 50, 255, cv2.THRESH_BINARY)
# text = pytesseract.image_to_string(thresh)
# print("Top UI text from the given coordinates:", text)

# picz = pyautogui.screenshot(
#     region=(left, (top + height), width, height-105))
# picz.save(os.path.join(screenshots_path, "screenshot_2.png"))
# pic2 = cv2.imread(os.path.join(screenshots_path, "screenshot_2.png"))
# gray_pic2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
# x, thresh2 = cv2.thrseshold(gray_pic2, 50, 255, cv2.THRESH_BINARY)
# text = pytesseract.image_to_string(thresh2)
# print("Bottom UI text from the given coordinates:", text)

# s1 = screenshot_region_and_save(screenshots_path, left, top-30,
#                          width, height-105, filename="s1.png")
# ui_text = read_text_from_image(s1, threshold=50)
# print(ui_text)
