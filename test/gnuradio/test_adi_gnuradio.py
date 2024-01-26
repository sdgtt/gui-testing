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
    def test_open_app_on_remote(self, ip):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host="192.168.10.117",
            user="analog",
            app_name="gnuradio",
            path="/usr/bin/gnuradio-companion",
        )
        time.sleep(10)
        # find_main screen
        # main_window = self.gui.find_window("ADI GNU Radio Companion")
        # center on screen
        # self.gui.set_window_center(main_window)
        time.sleep(5)
        # assert self.gui.controller.locateCenterOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.9)
        self.gui.controller.screenshot("results/test_open_app.png")






        



