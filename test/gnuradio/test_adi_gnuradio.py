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
<<<<<<< HEAD
        time.sleep(delay)
        print("Test build: Check application title")
        # Find main screen
        found_window = None
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
=======
        time.sleep(15)
<<<<<<< HEAD
        # print([ self.gui.get_window_title(w) for w in self.gui.get_open_windows() ])
        # find_main screen
        main_window = self.gui.find_window("*untitled - GNU Radio Companion")
        # center on screen
        # self.gui.set_window_center(main_window)
        # time.sleep(30)
=======
        #find_main_screen
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))      
        # find_window_title
        self.gui.find_window("*untitled - GNU Radio Companion")
        # center on screen
        self.gui.set_window_center(main_window)
        time.sleep(30)
>>>>>>> aee7232 (added checking if window is open then check window title)
        self.gui.controller.screenshot("results/test_open_app.png")
        assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.5)
        self.gui.alert('Try alert message function')





        

>>>>>>> 330962e (Revert "add result image")

        # Attempt to find the window titles
        for w in self.gui.get_open_windows():
            if self.gui.get_window_title(w) == "untitled - GNU Radio Companion":
                found_window = self.gui.find_window("untitled - GNU Radio Companion")
                break
            elif self.gui.get_window_title(w) == "*untitled - GNU Radio Companion":
                found_window = self.gui.find_window("*untitled - GNU Radio Companion")
                break
        # Perform actions based on the found window
        if found_window:
            print(found_window)
            assert self.gui.controller.locateOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.9)
            time.sleep(delay)
            # Take a screenshot of the main screen
            print("Test build: Taking screenshot for reference")
            self.gui.controller.screenshot("results/test_open_app.png")            
            print("Screenshot matches the reference image.")
            print("Testing done.")
        else:
            print("Application is not found")
                

    