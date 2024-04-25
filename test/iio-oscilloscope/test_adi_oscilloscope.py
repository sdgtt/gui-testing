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
        time.sleep(delay)
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
                window_active_screen_mapping.append((title, active_screen_title))
        time.sleep(delay)
        # Iterate through window-active screen mappings and find the active screen for each application
        for window_title, active_screen_title in window_active_screen_mapping:
            found_screen = None
            for window, title in open_windows:
                if title == window_title:
                    found_screen = self.gui.find_window(active_screen_title)
                    break
        time.sleep(delay)
            # Perform actions based on the found screen
            if found_screen:
                print(found_screen)
                # Perform actions specific to the active screen
                # For example, take a screenshot or perform an assertion
                assert self.gui.controller.locateOnScreen("ref_test_active_screen.png", grayscale=True, confidence=0.9)
                time.sleep(delay)
                # Take a screenshot of the active screen
                print(f"Test build: Taking screenshot for {window_title}")
                self.gui.controller.screenshot(f"results/test_{window_title.replace(' ', '_')}_active_screen.png")            
                print("Screenshot matches the reference image.")
                print("Testing done.")
            else:
                print(f"Active screen not found for {window_title}")