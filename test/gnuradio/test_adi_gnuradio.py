import pytest
import pyguit
import time
import os
import shutil

class TestADIGnuradio:

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
            host= ip,
            user="analog",
            app_name="gnuradio",
            path="/usr/bin/gnuradio-companion",
        )
        time.sleep(15)
        #find_main_screen
        # for w in self.gui.get_open_windows():
        #     if w:
        #         print(self.gui.get_window_title(w))      
        # # find_window_title
        # try:  
        #     # for 2022R2
        #     self.gui.find_window("untitled - GNU Radio Companion")
        # except:
        #     try:
        #         # for Kuiper 2.0
        #         self.gui.find_window("*untitled - GNU Radio Companion")
        #     except:
        #         print("Application title not found")
        # time.sleep(30)
        # self.gui.controller.screenshot("results/test_open_app.png")
        # assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.5)

        try:
            # for 2022R2
            found_window_title = "untitled - GNU Radio Companion"
            self.gui.find_window(found_window_title)
        except:
            try:
                # for Kuiper 2.0
                found_window_title = "*untitled - GNU Radio Companion"
                self.gui.find_window(found_window_title)
            except:
                found_window_title = None  # Window not found

        # Get titles of open windows
        open_window_titles = []  # List to store titles of open windows
        for w in self.gui.get_open_windows():
            if w:
                open_window_titles.append(self.gui.get_window_title(w))

        # Print the titles obtained from get_open_windows()
        print("Titles obtained from get_open_windows():")
        print(open_window_titles)

        # Check if the found window title matches any of the open windows
        if found_window_title:
            if found_window_title in open_window_titles:
                print(f"Window with title '{found_window_title}' found and matches the open windows.")
            else:
                print(f"Window with title '{found_window_title}' found but does not match any of the open windows.")
        else:
            print("Application title not found")

        time.sleep(30)
        self.gui.controller.screenshot("results/test_open_app.png")
        assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.5)




        



