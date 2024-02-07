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
        print([ self.gui.get_window_title(w) for w in self.gui.get_open_windows() ])
        # find_main screen
        # main_window = self.gui.find_window("untitled - GNU Radio Companion")
        # center on screen
        # self.gui.set_window_center(main_window)
        time.sleep(delay)
        assert self.gui.controller.locateAllOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.5)
        self.gui.controller.screenshot("results/test_open_app.png")
        # self.gui.alert('Try alert message function')





        



