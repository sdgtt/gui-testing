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
        time.sleep(20)
        #find_active_screen
        for w in self.gui.get_open_windows():
            if w:   
                print(self.gui.get_window_title(w))
        #         print(self.gui.get_window_geometry(w))
        time.sleep(delay)
        self.gui.find_window("ADI IIO Oscilloscope")
        time.sleep(delay)
        self.gui.controller.screenshot("results/test_open_a_app.png")
        #         # print(self.gui.set_window_position(w))
        # try:
        #     self.gui.find_wi
        #     self.gui.find_window("ADI IIO Oscilloscope - Capture1")
        # except:
        #     print("Application window not found")
        # else:
        #     self.gui.find_window("ADI IIO Oscilloscope - Capture1")
        #     self.gui.find_window("ADI IIO Oscilloscope - Capture1")

        
        
        # time.sleep(delay)
        # self.gui.controller.screenshot("results/test_open_a_app.png")
        # assert self.gui.controller.locateOnScreen("ref_test_open_a_app.png", grayscale=True, confidence=0.5)
         
        # time.sleep(delay)
        # assert self.gui.controller.locateOnScreen("ref_test_open_a_app.png", grayscale=True, confidence=0.5)
            
                # print(self.gui.get_window_title("ADI IIO Oscilloscope - Capture1"))
                # time.sleep(delay)
                # self.gui.find_window("ADI IIO Oscilloscope - Capture1")
                # time.sleep(delay)
                # self.gui.controller.screenshot("results/test_open_b_app.png")
                # time.sleep(delay)
        # find_main_window
        # self.gui.find_window("ADI IIO Oscilloscope")
        # time.sleep(delay)
        # # self.gui.find_window("ADI IIO Oscilloscope - Capture1")
        # # time.sleep(delay)
        # self.gui.controller.screenshot("results/test_open_a_app.png")
        # time.sleep(delay)
        # # self.gui.controller.screenshot("results/test_open_b_app.png")
        # # time.sleep(delay)
        # assert self.gui.controller.locateAllScreen("ref_test_open_a_app.png", grayscale=True, confidence=0.5)
        # time.sleep(delay)
        # assert self.gui.controller.locateAllScreen("ref_test_open_b_app.png", grayscale=True, confidence=0.5)