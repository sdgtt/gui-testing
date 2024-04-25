"""Class for managing GUI-based access"""

import logging
import os
import signal
import threading
import multiprocessing
import time
import subprocess
import re
from Xlib import display, X, Xatom
from ewmh import EWMH

from sys import platform
if not (platform == "linux" or platform == "linux2"):
    raise Exception("pyguit supports X systems for now")

log = logging.getLogger(__name__)

class gui:
    """GUI controller and helper methods"""

    def __init__(self):        
        try:
            if not 'DISPLAY' in os.environ:
                raise Exception("Display not present")
        except Exception:
            log.warning("Host is headless, will create a virtual display")
            from pyvirtualdisplay import Display
            self._display = Display(
                backend="xvnc",
                size=(1980,1080),
                color_depth=16
            ).start()

        import pyautogui
        self.controller = pyautogui
        self.xlib_display = display.Display(self.display_id)
        self.ewmh = EWMH(self.xlib_display)

    def __del__(self):
        if hasattr(self, "_display"):
            self._display.stop()

    @property
    def display(self):
        return self._display

    @property
    def display_id(self):
        return os.environ['DISPLAY']

    def run(self, desc, process, daemon=False):
        def task(p):
            output, errors = p.communicate()
            with open(f"{desc}.log","w") as logfile:
                logfile.write(output)
            with open(f"{desc}_err.log","w") as errfile:
                errfile.write(errors)

        x = threading.Thread(target=task, args=(process,), daemon=daemon)
        x.start()
        setattr(self, f"process_{desc}", process)

    def stop(self, desc):
        if hasattr(self, f"process_{desc}"):
            getattr(self,f"process_{desc}").kill()
            return
        raise Exception(f"Cannot stop process_{desc} since not started")


    def attach_openbox(self):
        p = subprocess.Popen(["openbox-session"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
        self.run("openbox",p, daemon=True)

    def dettach_openbox(self):
        self.stop("openbox")

    def find_window(self, title):
        windows = self.get_open_windows()
        for window in windows:
            _w = self.get_window_title(window)
            if _w == title:
                return window
        raise Exception(f"Cannot find {title}")

    def close_window(self, window):
        window.destroy()
    
    def get_open_windows(self):
        root = self.xlib_display.screen().root
        # Get all children windows of the root window
        windows = root.query_tree().children
        open_windows = []
        for window in windows:
            # Check if the window is mapped (visible)
            _window = None
            if window.get_attributes().map_state == X.IsViewable:
                if self.get_window_title(window):
                    _window = window
                else:
                    sub_children = window.query_tree().children
                    for sb_window in sub_children:
                        if self.get_window_title(sb_window):
                            _window = sb_window
                open_windows.append(_window)
        return open_windows

    def get_window_title(self, window):
        if window:
            window_name = window.get_property(Xatom.WM_NAME , X.AnyPropertyType, 0, 1024)
            if window_name:
                if isinstance(window_name.value, str):
                    return window_name.value
                return window_name.value.decode("utf-8")
        return None
    
    def get_window_position(self, window):
        # Implement logic to obtain window position
        # For demonstration purposes, we'll return dummy coordinates
        return 100, 100, 800, 600

    def frame(self, window):
        frame = window
        while frame.query_tree().parent != self.ewmh.root:
            frame = frame.query_tree().parent
        return frame

    def get_window_geometry(self, window):
        return self.frame(window).get_geometry()

    def set_window_position(self, window, new_x, new_y):
        self.ewmh.setMoveResizeWindow(
            win=self.frame(window),
            x=new_x,
            y=new_y,
            w=None,
            h=None,
        )
        self.ewmh.display.flush()

    def set_active_window(self, window):
        self.ewmh.setActiveWindow(window)
        self.ewmh.display.flush()

    def set_window_above(self, window):
        self.set_active_window(window)
        self.ewmh.setWmState(window, 1, "_NET_WM_STATE_ABOVE")
        self.ewmh.display.flush()

    def set_window_center(self, window):
        self.set_active_window(window)
        wgeo = self.get_window_geometry(window)
        self.set_window_position(
            window,
            new_x=int(1980/2)-int(wgeo.width/2),
            new_y=int(1080/2)-int(wgeo.height/2),
        )

    def open_app(self, app_name, path, host=None, user=None, daemon=True):
        command = [path]
        if host:
            command = ["ssh","-X", f"{user}@{host}", path]

        p = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                            )
        self.run(app_name,p, daemon=daemon)

if __name__ == "__main__":
    g = gui()
    time.sleep(10)
    print(g.display_id)

    g.attach_openbox()
    g.open_app(
            host="192.168.10.181",
            user="analog",
            app_name="aditof_demo.py",
            path="/home/analog/Desktop/aditof-demo.sh",
        )
    time.sleep(5)
    for w in g.get_open_windows():
        if w:
            print(g.get_window_title(w))
            print(g.get_window_geometry(w))
            g.set_window_position(w,800,20)
            time.sleep(5)
            print(g.get_window_geometry(w))
            time.sleep(5)

    w = g.find_window("aditof-demo 3.1.0")
    print(g.get_window_title(w))
    g.close_window(w)
    del g
