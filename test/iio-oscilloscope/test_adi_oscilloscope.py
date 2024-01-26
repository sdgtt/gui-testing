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

    def test_open_app(self):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host="192.168.10.150",
            user="analog",
            app_name="osc",
            path="/usr/local/bin/iio_oscilloscope",
        )
        time.sleep(10)
        # find_main screen
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        main_window = self.gui.find_window("ADI IIO Oscilloscope")
        # center on screen
        self.gui.set_window_center(main_window)
        time.sleep(5)
        assert self.gui.controller.locateCenterOnScreen("ref_osc_main.png", grayscale=True, confidence=0.9)
        self.gui.controller.screenshot("results/test_open_app.png")
         @pytest.mark.remote

    def test_open_app_on_remote(self, ip):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host=ip,
            user="analog",
            app_name="osc",
            path="/home/analog/Workspace/aditof_sdk/build/examples/aditof-demo/aditof-demo",
        )
        time.sleep(10)
        # find_main screen
        main_window = self.gui.find_window("aditof-demo 3.1.0")
        # center on screen
        self.gui.set_window_center(main_window)
        time.sleep(5)
        assert self.gui.controller.locateCenterOnScreen("ref_test_open_app.png", grayscale=True, confidence=0.9)
        self.gui.controller.screenshot("results/test_open_app.png")
def test_play_button(self):
        '''Test if capture works by clicking the play button'''
        found = self.gui.controller.locateCenterOnScreen("ref_test_play_button.png", grayscale=True, confidence=0.9)
        assert found
        self.gui.controller.click(found)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_play_button.png")

    def test_capture_rgb(self):
        '''Check if RGB window opens'''
        rgb_window = self.gui.find_window("Rgb Image")     
        self.gui.set_window_above(rgb_window)
        self.gui.set_window_center(rgb_window)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_capture_rgb.png")
        

    def test_capture_ir(self):
        '''Check if IR window opens'''
        ir_window = self.gui.find_window("IR Image")     
        self.gui.set_window_above(ir_window)
        self.gui.set_window_center(ir_window)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_capture_ir.png")

    def test_capture_depth(self):
        '''Check if depth window opens and verify with a reference image'''
        depth_window = self.gui.find_window("Depth Image")
        self.gui.set_window_above(depth_window)     
        self.gui.set_window_center(depth_window)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_capture_depth.png")
        # try to compare with ref data
        found = self.gui.controller.locateOnScreen('ref_depth_win.png', confidence=0.7)
        assert found
        self.gui.controller.screenshot("results/test_capture_depth_raw.png",region=found)


    def test_stop_button(self):
        '''Stop capture by clicking stop button'''
        main_window = self.gui.find_window("aditof-demo 3.1.0")
        self.gui.set_window_above(main_window)
        self.gui.set_window_center(main_window)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_stop_button_before.png")
        found = self.gui.controller.locateCenterOnScreen("ref_test_stop_button.png", grayscale=True, confidence=0.9)
        assert found
        self.gui.controller.click(found)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_stop_button_after.png")

    @pytest.mark.local
    def test_kill_adi_tof_server(self,ip):
        # manually kill aditof-server (for now)
        self.gui.open_app(
            host=ip,
            user="analog",
            app_name="aditof-server-killer",
            path="/home/analog/Workspace/aditof_sdk/build/apps/server/aditof-server-killer",
            daemon=False
        )






        


