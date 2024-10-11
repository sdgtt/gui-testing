import pytest
import pyguit
import time
import os
import shutil

class TestIIOOscilloscope:

    @classmethod
    def setup_class(self):
        '''Setup the pyguit object. Will be called once before the start of test'''
        self.gui = pyguit.gui()
        self.gui.attach_openbox()
        # self.gui.run_ssh_agent()
        time.sleep(10)
        try:
            os.makedirs("results")
        except FileExistsError:
            # directory already exists
            shutil.rmtree('results')
            os.makedirs("results")
        
    @classmethod
    def teardown_class(self):
        '''Garbage collector. Will be called once after running of tests'''
        time.sleep(10)
        self.gui.dettach_openbox()
        del self.gui

    @pytest.mark.remote
    def test_open_app_on_remote(self, ip, delay):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host=ip,
            user="analog",
            app_name="osc",
            path="/usr/local/bin/osc",
        )
        time.sleep(delay)
        print("Test build: Check application title")
        # Find main screen
        found_window = None
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        time.sleep(delay)
        # find_main screen
        main_window = self.gui.find_window("ADI IIO Oscilloscope - Capture1")
        self.gui.set_window_center(main_window)
        time.sleep(delay)
        assert self.gui.controller.locateCenterOnScreen("ref_test_open_adi_iio_oscilloscope-capture1_app.png", grayscale=True, confidence=0.5)
        self.gui.controller.screenshot("results/test_open_adi_iio_oscilloscope-capture1_app.png")
         # find_main screen
        time.sleep(delay)
        second_window = self.gui.find_window("ADI IIO Oscilloscope")
        self.gui.set_window_center(second_window)
        time.sleep(delay)
        assert self.gui.controller.locateCenterOnScreen("ref_test_open_adi_iio_oscilloscope_app.png", grayscale=True, confidence=0.5)
        self.gui.controller.screenshot("results/test_open_adi_iio_oscilloscope_app.png")
    def test_play_button(self):
        '''Test if capture works by clicking the play button'''
        found = self.gui.controller.locateCenterOnScreen("ref_test_play_button.png", grayscale=True, confidence=0.9)
        assert found
        self.gui.controller.click(found)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_play_button.png")    
        # List to store the window-active screen mappings
        # print("Test build: Window mapping")

        # window_active_screen_mapping = []

        # # Define the active screen titles for each window title
        # for window, title in open_windows:
        #     active_screen_title = None
        #     # Define the active screen title based on the window title
        #     if title == "ADI IIO Oscilloscope":
        #         active_screen_title = "Active Screen 1"
        #     elif title == "ADI IIO Oscilloscope - Capture1":
        #         active_screen_title = "Active Screen 2"
        #     # Add the window title and its associated active screen title to the mapping list
        #     if active_screen_title:
        #         window_active_screen_mapping.append((window, title, active_screen_title))

        # print("Test build: Window position coordinates")

        # # Iterate through window-active screen mappings and find the position coordinates for each application window
        # for window, window_title, active_screen_title in window_active_screen_mapping:
        #     if window:
        #         # Capture a screenshot within the application window coordinates
        #         screenshot_path = f"results/test_{window_title.replace(' ', '_')}_active_screen.png"
        #         # Get the position and size of the application window
        #         x, y, width, height = self.gui.get_window_position(window)
        #         # Move the mouse to the top-left corner of the application window
        #         self.gui.controller.moveTo(x, y)
        #         # Capture a screenshot of the specified region
        #         self.gui.controller.screenshot(screenshot_path, region=(x, y, width, height))
        #         # Print a message indicating successful screenshot capture
        #         print(f"Screenshot captured for {window_title}.")
        #         # Perform assertions to compare the captured screenshot with reference images
        #         reference_image = f"ref_test_open_{window_title.lower()[0]}_app.png"  # Construct reference image title
        #         assert pyautogui.locateOnScreen(reference_image, region=(x, y, width, height), grayscale=True, confidence=0.9)
        #         # Print a message indicating successful comparison
        #         print(f"Screenshot for {window_title} matches the reference image.")
        #     else:
        #         print(f"Window not found for {window_title}.")