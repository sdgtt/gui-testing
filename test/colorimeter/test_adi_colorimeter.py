import pytest
import pyguit
import time
import os
import shutil

class TestADIColorimeter:

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

    def test_open_app(self):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host="192.168.10.150",
            user="analog",
            app_name="adi_colorimeter",
            path="/usr/local/bin/adi_colorimeter",
        )
        time.sleep(10)
        # find_main screen
        main_window = self.gui.find_window("aditof-demo 3.1.0")
        # center on screen
        self.gui.set_window_center(main_window)
        time.sleep(5)
        assert self.gui.controller.locateCenterOnScreen("ref_colorimeter_main.png", grayscale=True, confidence=0.9)
        self.gui.controller.screenshot("results/test_open_app.png")







        







