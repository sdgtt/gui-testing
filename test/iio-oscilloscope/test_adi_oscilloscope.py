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
        #find_small_window
        time.sleep(delay)
        small_window = self.gui.find_window("ADI IIO Oscilloscope")
        self.gui.set_window_center(small_window)
        print("Test build: Done small window")
        time.sleep(delay)
        assert self.gui.controller.locateCenterOnScreen("ref_test_open_adi_iio_oscilloscope_app.png", grayscale=True, confidence=0.5)
        self.gui.controller.screenshot("results/test_open_adi_iio_oscilloscope_app.png")
        # find_main screen
        main_window = self.gui.find_window("ADI IIO Oscilloscope - Capture1")
        self.gui.set_window_center(main_window)
        time.sleep(delay)
        assert self.gui.controller.locateCenterOnScreen("ref_test_open_adi_iio_oscilloscope-capture1_app.png", grayscale=True, confidence=0.5)
        self.gui.controller.screenshot("results/test_open_adi_iio_oscilloscope-capture1_app.png")
        print("Test build: Done main window")
        
    def test_play_button(self,delay):
        '''Test if capture works by clicking the checkbox button'''
        checkboxBtn = self.gui.controller.locateCenterOnScreen("ref_test_enable_all_checkbox.png", grayscale=True, confidence=0.9)
        assert checkboxBtn
        self.gui.controller.click(checkboxBtn)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_checkbox_button.png")   
        print("Test build: Done checkbox")
        time.sleep(delay)
        runBtn = self.gui.controller.locateCenterOnScreen("ref_test_run_button.png", grayscale=True, confidence=0.5)
        assert runBtn
        self.gui.controller.click(runBtn)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_run_button.png") 
        print("Test build: Done run button")

      