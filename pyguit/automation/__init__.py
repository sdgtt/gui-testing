"""Automation subpackage - GUI control and window management."""

from pyguit.automation.controller import GUIController
from pyguit.automation.exceptions import (
    DisplayNotAvailableError,
    PlatformNotSupportedError,
    ProcessNotFoundError,
    PyGUItError,
    ValidationError,
    WindowNotFoundError,
)

__all__ = [
    "GUIController",
    "DisplayNotAvailableError",
    "PlatformNotSupportedError",
    "ProcessNotFoundError",
    "PyGUItError",
    "ValidationError",
    "WindowNotFoundError",
]
