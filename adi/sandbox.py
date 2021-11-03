import os
import pyautogui
import pytesseract
import cv2
import time
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = os.path.join(os.getcwd(), "scopy_images")

img = os.path.join(image_path, "m2k_usb.png")
image = cv2.imread(img)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
x, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

# Crop images
crop_top = image[0:30, 0:150]
crop_bottom = image[160:193, 0:150]

# Threshold cropped images
x, thresh_top = cv2.threshold(crop_top, 90, 255, cv2.THRESH_BINARY)
y, thresh_bottom = cv2.threshold(crop_bottom, 90, 255, cv2.THRESH_BINARY)

# Print shapes
# print(type(image))  # <class 'numpy.ndarray'>
# print(image.shape)

ref = pytesseract.image_to_string(thresh)
print(f"Texts in Threshed Image: {ref}")

if "ip:192" in ref:
    print("IP Connected")
elif "ip:127" in ref:
    print("Demo Mode")
elif "usb" in ref:
    print("Serially Connected")

# Show images
# cv2.imshow("Image", image)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Cropped Top", crop_top)
# cv2.imshow("Cropped Bottom", crop_bottom)
# cv2.imshow("Thresh Cropped Top", thresh_top)
# cv2.imshow("Thresh Cropped Bottom", thresh_bottom)
cv2.imshow("Threshold", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
