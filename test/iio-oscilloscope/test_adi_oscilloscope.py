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
       open_windows = [(w, self.gui.get_window_title(w)) for w in self.gui.get_open_windows() if w]

    # Print the titles of open windows
    for window, title in open_windows:
        print(title)
    time.sleep(delay)

    # List to store the window-active screen mappings
    window_active_screen_mapping = []

    # Define the active screen titles for each window title
    for window, title in open_windows:
        active_screen_title = None
        # Define the active screen title based on the window title
        if title == "ADI IIO Oscilloscope":
            active_screen_title = "Active Screen 1"
        elif title == "ADI IIO Oscilloscope - Capture1":
            active_screen_title = "Active Screen 2"
        # Add the window title and its associated active screen title to the mapping list
        if active_screen_title:
            window_active_screen_mapping.append((window, title, active_screen_title))

    # Iterate through window-active screen mappings and find the position coordinates for each application window
    for window, window_title, active_screen_title in window_active_screen_mapping:
        if window:
            # Get the position coordinates of the application window
            window_position = self.gui.get_window_position(window)
            if window_position:
                # Extract the position coordinates
                x, y, width, height = window_position
                # Capture a screenshot within the application window coordinates
                screenshot_path = f"results/test_{window_title.replace(' ', '_')}_active_screen.png"
                self.gui.controller.screenshot(screenshot_path, region=(x, y, width, height))
                # Print a message indicating successful screenshot capture
                print(f"Screenshot captured for {window_title}.")
                # Perform assertions to compare the captured screenshot with reference images
                reference_image = f"ref_test_open_{window_title.lower()[0]}_app.png"  # Construct reference image title
                assert self.gui.controller.locateOnScreen(reference_image, region=(x, y, width, height), grayscale=True, confidence=0.9)
                # Print a message indicating successful comparison
                print(f"Screenshot for {window_title} matches the reference image.")
            else:
                print(f"Failed to get position coordinates for {window_title}.")
        else:
            print(f"Window not found for {window_title}.")