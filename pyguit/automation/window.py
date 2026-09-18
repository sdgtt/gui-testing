from __future__ import annotations

import logging
from typing import Any

from pyguit.automation.exceptions import WindowNotFoundError

log = logging.getLogger(__name__)


class WindowManager:
    """X11 window management via Xlib and EWMH. Linux-only."""

    def __init__(self, display_id: str) -> None:
        from Xlib import display, X, Xatom
        from ewmh import EWMH

        self._X = X
        self._Xatom = Xatom
        self._xlib_display = display.Display(display_id)
        self._ewmh = EWMH(self._xlib_display)

    def find_window(self, title: str) -> Any:
        for window in self.get_open_windows():
            if self.get_window_title(window) == title:
                return window
        raise WindowNotFoundError(f"Cannot find window '{title}'")

    def get_open_windows(self) -> list[Any]:
        root = self._xlib_display.screen().root
        windows = root.query_tree().children
        result: list[Any] = []
        for window in windows:
            if window.get_attributes().map_state != self._X.IsViewable:
                continue
            if self.get_window_title(window):
                result.append(window)
            else:
                for child in window.query_tree().children:
                    if self.get_window_title(child):
                        result.append(child)
        return result

    def get_window_title(self, window: Any) -> str | None:
        if window is None:
            return None
        prop = window.get_property(
            self._Xatom.WM_NAME, self._X.AnyPropertyType, 0, 1024
        )
        if prop is None:
            return None
        if isinstance(prop.value, str):
            return prop.value
        return prop.value.decode("utf-8")

    def get_window_geometry(self, window: Any) -> Any:
        return self._get_frame(window).get_geometry()

    def get_window_position(self, window: Any) -> tuple[int, int, int, int]:
        geo = self.get_window_geometry(window)
        return (geo.x, geo.y, geo.width, geo.height)

    def set_window_position(self, window: Any, x: int, y: int) -> None:
        self._ewmh.setMoveResizeWindow(
            win=self._get_frame(window),
            x=x,
            y=y,
            w=None,
            h=None,
        )
        self._ewmh.display.flush()

    def set_active_window(self, window: Any) -> None:
        self._ewmh.setActiveWindow(window)
        self._ewmh.display.flush()

    def set_window_above(self, window: Any) -> None:
        self.set_active_window(window)
        self._ewmh.setWmState(window, 1, "_NET_WM_STATE_ABOVE")
        self._ewmh.display.flush()

    def set_window_center(
        self, window: Any, screen_width: int, screen_height: int
    ) -> None:
        self.set_active_window(window)
        geo = self.get_window_geometry(window)
        self.set_window_position(
            window,
            x=screen_width // 2 - geo.width // 2,
            y=screen_height // 2 - geo.height // 2,
        )

    def close_window(self, window: Any) -> None:
        window.destroy()

    def _get_frame(self, window: Any) -> Any:
        frame = window
        while frame.query_tree().parent != self._ewmh.root:
            frame = frame.query_tree().parent
        return frame
