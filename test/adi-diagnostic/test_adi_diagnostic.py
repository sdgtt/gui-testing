import pytest
import pyguit
import time
import os
import shutil

class TestDiagnostic:

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
    def test_open_app_terminal_on_remote(self, ip, delay):
        '''Test if app opens, and checks main window'''
        self.gui.open_app(
            host=ip,
            user="analog",
            app_name="adi_diagnostic_report",
            path="/usr/local/bin/adi_diagnostic_report --gui")
        time.sleep(delay)
        print("Test build: Check application title")
        # Find main screen
        found_window = None
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        print("Test build: Check application title")
        #Find main screen
        found_window = None
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        time.sleep(delay)
        self.gui.find_window("Generate Diagnostic Report")
        print("Test build: Done main window")
        time.sleep(delay)
        assert self.gui.controller.locateOnScreen("ref_test_open_diagnostic.png", grayscale=True, confidence=0.9)
        self.gui.controller.screenshot("results/test_open_diagnostic.png")
      
        
    def test_run_button(self,delay):
        '''Test if capture works by clicking the checkbox button'''
        noneBtn = self.gui.controller.locateCenterOnScreen("ref_test_click_none_button.png", grayscale=True, confidence=0.9)
        assert noneBtn
        self.gui.controller.click(noneBtn)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_click_none_button.png")   
        print("Test build: Done None button")
        time.sleep(delay)
        analogItem = self.gui.controller.locateCenterOnScreen("ref_test_click_analog.png", grayscale=True, confidence=0.9)
        assert analogItem
        self.gui.controller.click(analogItem)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_click_analog.png") 
        print("Test build: Done analog item")
        generateBtn = self.gui.controller.locateCenterOnScreen("ref_test_click_generate_button.png", grayscale=True, confidence=0.9)
        assert generateBtn
        self.gui.controller.click(generateBtn)
        time.sleep(5)
        self.gui.controller.screenshot("results/test_generate_button.png")   
        print("Test build: Done Generate button")
        

      