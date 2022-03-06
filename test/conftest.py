import adi
import os
import pytest
import shutil
import subprocess
import time
from test.common import (
    image_path,
    screenshot_region,
    locate_and_click_image,
    locate_image_with_str,
)
from test.scopy_test import *

scopy_popup_path = os.path.join(image_path, "Scopy_auto_update_popup.png")


#########################################
# Hooks
def pytest_addoption(parser):
    parser.addoption(
        "--software-path",
        action="store",
        default="",
        help="Path to the application's executable",
    )
    # parser.addoption(
    #     "--windows",
    #     action="store_true",
    #     help="The OS used by the application under test is Windows."
    # )
    # parser.addoption(
    #     "--linux",
    #     action="store_true",
    #     help="The OS used by the application under test is Linux."
    # )


def pytest_generate_tests(metafunc):
    if "software_path" in metafunc.fixturenames:
        metafunc.parametrize(
            "software_path", [metafunc.config.getoption("--software-path")]
        )


#########################################
# Fixtures
@pytest.fixture(autouse=True)
def access_software_windows(request, software_path):
    # Setup
    app_name = os.path.basename(software_path)

    # Delete the Scopy *.ini file from the previous settings made
    if os.path.splitext(app_name)[0].lower() == "scopy":
        username = os.getlogin()
        dir = f"C:\\Users\\{username}\\AppData\\Roaming\\ADI"
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            try:
                os.mkdir(dir)
            except Exception as e:
                print(e)
        else:
            os.mkdir(dir)

    # Open the application
    if os.path.isfile(software_path):
        os.startfile(str(software_path))
        time.sleep(10)
    else:
        raise Exception("The path given is not an executable.")

    yield

    # Teardown
    # Terminate the application
    subprocess.check_output(
        f"TASKKILL /F /IM {app_name}", shell=True, stderr=subprocess.STDOUT)

    # Delete the ADI folder if the app_name is Scopy
    if os.path.splitext(app_name)[0].lower() == "scopy":
        try:
            shutil.rmtree(dir)
        except Exception as e:
            print(e)
    time.sleep(5)


@pytest.fixture()
def access_software_linux(request, software_path):
    # Setup
    base_name = os.path.basename(software_path)
    app_name = os.path.splitext(base_name)[0]

    subprocess.run(f"{app_name} &", shell=True, check=True)
    a = subprocess.run("echo $!", shell=True, capture_output=True)
    PID = a.stdout.decode()
    yield
    # Teardown
    subprocess.run(f"kill -15 {PID}", shell=True, check=True)
    time.sleep(1)
    subprocess.run(f"kill -9 {PID}", shell=True, check=True)


@pytest.fixture()
def test_popup_dialog_box(request, app_name="scopy", popup_img_path=scopy_popup_path, cmd="close"):
    """test_popup_dialog_box: Interacts with the Automatic Update Dialog box in Scopy

    parameter:
        app_name: type=string
            Name of the software that is being tested
            Options: scopy
        popup_img_path: type=path
            Absolute/relative path of the reference pop-up image
        cmd: type=string
            Interaction needed for the dialog box.
            Options: yes, no, close
    """
    try:
        popup = pyautogui.locateCenterOnScreen(popup_img_path, confidence=0.8)
        if popup:
            locate_and_click_image(popup_img_path)
            print("Pop-up clicked!")

        if "scopy" in app_name.lower():
            if cmd.lower() == "yes":
                yes_img = os.path.join(image_path, "Scopy_yes.png")
                locate_and_click_image(yes_img)
            elif cmd.lower() == "no":
                no_img = os.path.join(image_path, "Scopy_no.png")
                locate_and_click_image(no_img, confidence_level=0.8)
            elif cmd.lower() == "close":
                close_img = os.path.join(image_path, "Scopy_close.png")
                locate_and_click_image(close_img)
            time.sleep(3)
    except Exception as e:
        raise Exception(e)
    yield


@pytest.fixture()
def test_screenshot_region(request):
    yield screenshot_region


@pytest.fixture()
def test_locate_and_click_image(request):
    yield locate_and_click_image


@pytest.fixture()
def test_locate_image_with_str(request):
    yield locate_image_with_str


@pytest.fixture()
def test_scopy_add_device(request):
    yield scopy_add_device


@pytest.fixture()
def test_scopy_add_plus(request):
    yield scopy_add_plus


@pytest.fixture()
def test_scopy_choose_device(request):
    yield scopy_choose_device


@pytest.fixture()
def test_scopy_calibrate(request):
    yield scopy_calibrate


@pytest.fixture()
def test_scopy_connect(request):
    yield scopy_connect


@pytest.fixture()
def test_scopy_disconnect(request):
    yield scopy_disconnect


@pytest.fixture()
def test_scopy_disable_demo(request):
    yield scopy_disable_demo


@pytest.fixture()
def test_scopy_enable_demo(request):
    yield scopy_enable_demo


@pytest.fixture()
def test_scopy_forget_device(request):
    yield scopy_forget_device


@pytest.fixture()
def test_scopy_identify(request):
    yield scopy_identify


@pytest.fixture()
def test_scopy_register(request):
    yield scopy_register
