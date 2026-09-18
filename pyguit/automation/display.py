from __future__ import annotations

import logging
import os
import sys

from pyguit.automation.exceptions import DisplayNotAvailableError

log = logging.getLogger(__name__)

_IS_LINUX = sys.platform.startswith("linux")


class DisplayManager:
    """Manages display and virtual display lifecycle for headless environments."""

    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        color_depth: int = 16,
    ) -> None:
        self._width = width
        self._height = height
        self._color_depth = color_depth
        self._virtual_display = None

        if not _IS_LINUX:
            return

        if "DISPLAY" not in os.environ:
            log.warning("No DISPLAY set, creating virtual display")
            try:
                from pyvirtualdisplay import Display

                self._virtual_display = Display(
                    backend="xvnc",
                    size=(width, height),
                    color_depth=color_depth,
                )
                self._virtual_display.start()
            except Exception as exc:
                raise DisplayNotAvailableError(
                    f"Failed to create virtual display: {exc}"
                ) from exc

    @property
    def display_id(self) -> str:
        if "DISPLAY" in os.environ:
            return os.environ["DISPLAY"]
        raise DisplayNotAvailableError("No DISPLAY environment variable set")

    @property
    def screen_size(self) -> tuple[int, int]:
        return (self._width, self._height)

    @property
    def is_virtual(self) -> bool:
        return self._virtual_display is not None

    def stop(self) -> None:
        if self._virtual_display is not None:
            self._virtual_display.stop()
            self._virtual_display = None

    def __enter__(self) -> DisplayManager:
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
