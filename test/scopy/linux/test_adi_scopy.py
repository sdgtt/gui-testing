import pytest
import pyguit
import time
import os
import shutil

class TestScopy:

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
            app_name="flatpak",
            path="/usr/bin/flatpak",
        )
        time.sleep(delay)
        print("Test build: Check application title")
        # Find main screen
        found_window = None
        for w in self.gui.get_open_windows():
            if w:
                print(self.gui.get_window_title(w))
        print(self.gui.get_window_title(w))
        time.sleep(delay)

      