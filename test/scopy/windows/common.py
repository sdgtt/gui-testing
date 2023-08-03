import os
import time
import pyautogui
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = os.path.join(os.getcwd(), "adi", "scopy")
screenshots_path = os.path.join(os.getcwd(), "screenshots")


def prettify_move_and_click(x, y, t=1):
    """prettify_move_and_click: Prettify moving from one point to
    another and clicking it.

    parameters:
        x: type=int
            The x-coordinate of the point to go to and be clicked
        y: type=int
            The y-coordinate of the point to go to and be clicked
        t: type=int
            Time to move mouse over x-y coordinates
    """
    pyautogui.moveTo(x, y, t, pyautogui.easeOutQuad)
    pyautogui.click()


def read_text_from_image(path_to_shot, threshold_value=50):
    """read_text_from_image: Reads text from image/screenshot and returns it

    parameter:
        path_to_shot: type=path
            The path, filename,and extension of the saved screenshot
        threshold_value: type=int
            Anything equal or greater than this pixel value becomes
            lighter when processing the image to black and white
    """
    pic = cv2.imread(path_to_shot)
    gray_picture = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    i, thresh = cv2.threshold(
        gray_picture, threshold_value, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    return text


def compare_images(shot_path, *ref_imgs, show=False):
    """compare_images: Compares the UI screenshot to a number of reference images passed
    depending on the connection used.

    parameters:
        shot_path: type=path
            Path to the screenshot of the UI
        *ref_imgs: type=path/s
            Accepts a variable number of reference UI images to compare with the UI
            screenshot taken. This packs the path/s in a tuple named 'ref_imgs'.
        show: type=bool
            An option whether to open the result after comparing
    return:
        [max_location, bottom_right]: type=list of tuples
            A list containing the top-left and the bottom-righ corners found in the
            UI image
    """
    method = cv2.TM_CCOEFF_NORMED

    if ref_imgs:
        for path in ref_imgs:
            ui_img = cv2.imread(shot_path)
            ref_img = cv2.imread(path)
            ref_img_name = os.path.splitext(os.path.basename(path))[0]

            if ui_img.shape > ref_img.shape:
                # Apply Template Matching
                result = cv2.matchTemplate(ui_img, ref_img, method)
                _, _, _, max_location = cv2.minMaxLoc(result)

                # Top left corner of the ref_img found in the ui_img; (x, y)
                x, y = max_location

                # Bottom right corner of the ref_img found in the ui_img
                bottom_right = (x + ref_img.shape[1], y + ref_img.shape[0])

                print("ref_img_name:", ref_img_name)
                print("top left corner:", x, y)
                print("bottom_right:", bottom_right)

                if show:
                    cv2.rectangle(
                        ui_img, (x, y), bottom_right, (0, 255, 255), 5)
                    cv2.imshow(f"Comparison with {ref_img_name}", ui_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                yield [max_location, bottom_right]
            else:
                raise Exception(
                    "The UI Image to be used to search the reference/template image is smaller.")
    else:
        raise Exception("Include a path to the reference/template image.")


def screenshot_region(
    dir,
    filename="screenshot.png",
    show=False,
    left=0,
    top=0,
    width=1920,
    height=1080,
):
    """screenshot_region: Saves screenshot from pyautogui and
    returns the path, filename, and extension of the saved screenshot.
    The default values for the left, top, width, and height arguments
    are specified for 1920 by 1080 screen resolution.

    parameters:
        dir: type=path
            Path to where you want to save the screenshot
        filename: type=string
            Filename and extension for the screenshot
        show: type=bool
            An option whether to open the screenshot after saving
        left: type=int
            Left coordinate of the region to screenshot
        top: type=int
            Top coordinate of the region to screenshot
        width: type=int
            Width in pixels of the region to screenshot
        height: type=int
            Height in pixels of the region to screenshot
    return:
        file_path: type=path
            The path, filename,and extension of the saved screenshot
    """
    picture = pyautogui.screenshot(region=(left, top, width, height))
    file_path = os.path.join(dir, filename)
    picture.save(file_path)

    if show:
        img = cv2.imread(file_path)
        cv2.imshow(f"{filename}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return file_path


def locate_and_click_image(
    img_path,
    sleep_duration=2,
    confidence_level=0.8
):
    """locate_and_click_image: Locates the specified image in the UI
    and clicks it.

    parameters:
        img_path: type=path
            Absolute/relative path of the image
        confidence_level: type=int
            A scale that determines how accurate the image in the UI
            must be from that of the reference image
        duration: type=int
            Time sleep duration after executing the command in seconds
    """
    try:
        x, y = pyautogui.locateCenterOnScreen(
            img_path, confidence=confidence_level)
    except Exception as e:
        raise Exception(e)
    else:
        prettify_move_and_click(x, y)
        time.sleep(sleep_duration)


def locate_image_with_str(
    img_path,
    sleep_duration=2,
    confidence_level=0.8,
    threshold_value=130
):
    """locate_image_with_str: Locates the image with text in the UI,
    confirms it, and clicks it.

    parameters:
        img_path: type=path
            Absolute/relative path of the reference image
        confidence_level: type=int
            A scale that determines how accurate the image in the UI
            must be from that of the reference image
        threshold_value: type=int
            Anything equal or greater than this pixel value becomes
            lighter when processing the image to black and white
    """
    try:
        coord = pyautogui.locateOnScreen(img_path, confidence=confidence_level)
        l, t, w, h = coord
        # print("Located!")

        # Reads text from reference image
        reference_text = read_text_from_image(img_path, threshold_value)
        # print("Reference text read! Reference text:", reference_text)

        # Text, image seen on the UI
        picture_shot_path = screenshot_region(
            screenshots_path, left=l, top=t, width=w, height=h)
        ui_text = read_text_from_image(picture_shot_path, threshold_value)

        if ui_text.lower() == reference_text.lower():
            x, y = pyautogui.center(coord)
            prettify_move_and_click(x, y)
            time.sleep(sleep_duration)
        elif coord == None:
            raise Exception(
                "The image with text can't be found on the screen.")

    except Exception as e:
        raise Exception(e)
