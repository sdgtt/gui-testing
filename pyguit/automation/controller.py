from __future__ import annotations

import logging
import os
import sys
import time
from typing import Any

from pyguit.automation.exceptions import PlatformNotSupportedError
from pyguit.automation.process import ProcessManager

log = logging.getLogger(__name__)

_IS_LINUX = sys.platform.startswith("linux")


class GUIController:
    """Main facade for GUI automation. Cross-platform.

    On Linux: full window management via X11.
    On Windows: pyautogui-only mode (screenshots, clicks, OCR work;
    window find/move/center are unavailable).
    """

    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        color_depth: int = 16,
    ) -> None:
        self._width = width
        self._height = height

        self.processes = ProcessManager()
        self._display_manager = None
        self._window_manager = None

        if _IS_LINUX:
            from pyguit.automation.display import DisplayManager

            self._display_manager = DisplayManager(width, height, color_depth)

            try:
                from pyguit.automation.window import WindowManager

                self._window_manager = WindowManager(
                    self._display_manager.display_id
                )
            except Exception:
                log.warning("Could not initialize X11 window manager")

        import pyautogui

        self._pyautogui = pyautogui

    @property
    def is_linux(self) -> bool:
        return _IS_LINUX

    @property
    def is_windows(self) -> bool:
        return sys.platform == "win32"

    @property
    def screen_size(self) -> tuple[int, int]:
        if self._display_manager:
            return self._display_manager.screen_size
        return self._pyautogui.size()

    # --- Window management (Linux-only) ---

    def _require_window_manager(self) -> Any:
        if self._window_manager is None:
            raise PlatformNotSupportedError(
                "Window management requires Linux with X11. "
                "On Windows, use locate_on_screen() and capture_screenshot() instead."
            )
        return self._window_manager

    def find_window(self, title: str) -> Any:
        return self._require_window_manager().find_window(title)

    def get_open_windows(self) -> list[Any]:
        return self._require_window_manager().get_open_windows()

    def get_window_title(self, window: Any) -> str | None:
        return self._require_window_manager().get_window_title(window)

    def center_window(self, window: Any) -> None:
        wm = self._require_window_manager()
        w, h = self.screen_size
        wm.set_window_center(window, w, h)

    def focus_window(self, window: Any) -> None:
        self._require_window_manager().set_active_window(window)

    def raise_window(self, window: Any) -> None:
        self._require_window_manager().set_window_above(window)

    def move_window(self, window: Any, x: int, y: int) -> None:
        self._require_window_manager().set_window_position(window, x, y)

    def close_window(self, window: Any) -> None:
        self._require_window_manager().close_window(window)

    # --- Process management ---

    def launch_app(
        self,
        app_name: str,
        path: str,
        *,
        host: str | None = None,
        user: str | None = None,
        daemon: bool = True,
    ) -> Any:
        return self.processes.launch_app(
            app_name, path, host=host, user=user, daemon=daemon
        )

    def stop_app(self, name: str) -> None:
        self.processes.stop(name)

    def attach_openbox(self) -> None:
        self.processes.attach_openbox()

    def detach_openbox(self) -> None:
        self.processes.detach_openbox()

    # --- Input actions (cross-platform) ---

    def click(self, x: int, y: int) -> None:
        self._pyautogui.click(x, y)

    def double_click(self, x: int, y: int) -> None:
        self._pyautogui.doubleClick(x, y)

    def right_click(self, x: int, y: int) -> None:
        self._pyautogui.rightClick(x, y)

    def drag(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float = 0.5,
    ) -> None:
        self._pyautogui.moveTo(start_x, start_y)
        self._pyautogui.drag(
            end_x - start_x, end_y - start_y, duration=duration
        )

    def type_text(self, text: str, interval: float = 0.05) -> None:
        self._pyautogui.write(text, interval=interval)

    def press_key(self, key: str) -> None:
        self._pyautogui.press(key)

    def hotkey(self, *keys: str) -> None:
        self._pyautogui.hotkey(*keys)

    def move_to(self, x: int, y: int, duration: float = 0.25) -> None:
        self._pyautogui.moveTo(x, y, duration=duration)

    # --- Screen interaction (cross-platform) ---

    def locate_on_screen(
        self,
        image_path: str,
        confidence: float = 0.9,
        grayscale: bool = True,
    ) -> tuple[int, int] | None:
        try:
            result = self._pyautogui.locateCenterOnScreen(
                image_path, confidence=confidence, grayscale=grayscale
            )
            return result
        except self._pyautogui.ImageNotFoundException:
            return None

    def wait_for_image(
        self,
        image_path: str,
        timeout: float = 30.0,
        confidence: float = 0.9,
        interval: float = 0.5,
    ) -> tuple[int, int]:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.locate_on_screen(image_path, confidence=confidence)
            if result is not None:
                return result
            time.sleep(interval)
        raise TimeoutError(
            f"Image '{image_path}' not found within {timeout}s"
        )

    def capture_screenshot(
        self,
        filepath: str,
        region: tuple[int, int, int, int] | None = None,
    ) -> str:
        if region:
            screenshot = self._pyautogui.screenshot(region=region)
        else:
            screenshot = self._pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath

    # --- OCR-based interaction (cross-platform) ---

    def find_text(
        self,
        text: str,
        confidence: int = 40,
        screenshot_path: str | None = None,
    ) -> list[dict]:
        """Find text on screen using OCR. Returns list of matches with cx/cy coords."""
        from pyguit.ocr.reader import OCRReader

        cleanup = False
        if screenshot_path is None:
            import tempfile
            screenshot_path = os.path.join(
                tempfile.gettempdir(), "_pyguit_find_text.png"
            )
            self.capture_screenshot(screenshot_path)
            cleanup = True

        reader = OCRReader()
        matches = reader.find_text(
            screenshot_path, text, min_confidence=confidence
        )

        if cleanup:
            try:
                os.remove(screenshot_path)
            except OSError:
                pass

        return matches

    def click_text(
        self,
        text: str,
        confidence: int = 40,
        occurrence: int = 0,
    ) -> bool:
        """Find text on screen via OCR and click its center.

        Args:
            text: The text to find (case-insensitive, partial match).
            confidence: Minimum OCR confidence (0-100).
            occurrence: Which match to click if multiple found (0 = first).

        Returns:
            True if text was found and clicked, False otherwise.
        """
        matches = self.find_text(text, confidence=confidence)
        if not matches or occurrence >= len(matches):
            return False

        match = matches[occurrence]
        self._pyautogui.click(match["cx"], match["cy"])
        return True

    def wait_for_text(
        self,
        text: str,
        timeout: float = 30.0,
        interval: float = 1.0,
        confidence: int = 40,
    ) -> dict:
        """Wait until text appears on screen, then return its location.

        Returns the first match dict with cx/cy coords.
        Raises TimeoutError if not found within timeout.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            matches = self.find_text(text, confidence=confidence)
            if matches:
                return matches[0]
            time.sleep(interval)
        raise TimeoutError(
            f"Text '{text}' not found on screen within {timeout}s"
        )

    # --- Lifecycle ---

    def close(self) -> None:
        self.processes.stop_all()
        if self._display_manager:
            self._display_manager.stop()

    def __enter__(self) -> GUIController:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
