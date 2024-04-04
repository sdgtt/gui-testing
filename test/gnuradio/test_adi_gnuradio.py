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
        print("Test build: Started")
        '''Test if app opens, and checks main window'''
        print("Test build: Opening application")
        self.gui.open_app(
            host= ip,
            user="analog",
            app_name="gnuradio",
            path="/usr/bin/gnuradio-companion",
        )
        time.sleep(delay)
        print("Test build: Check application title")
        # Find main screen
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        #For 2022R2
        if found_window == self.gui.find_window("untitled - GNU Radio Companion"):
            print(found_window)
            assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.9)
            time.sleep(delay)
            # Take a screenshot of the main screen
            print("Test build: Taking screenshot for reference")
            self.gui.controller.screenshot("results/test_open_app.png")            
            print("Screenshot matches the reference image.")
            print("Testing done.")  
        #For Kuiper 2.0
        elif found_window == self.gui.find_window("*untitled - GNU Radio Companion"):
            print(found_window)
            assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.9)
            time.sleep(delay)
            # Take a screenshot of the main screen
            print("Test build: Taking screenshot for reference")
            self.gui.controller.screenshot("results/test_open_app.png")            
            print("Screenshot matches the reference image.")
            print("Testing done.")
        else:
            found_window = None 
            print("Application is not found")

    