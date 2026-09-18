import os
import sys
import tempfile

import pytest


class TestGUIControllerBasic:
    """Tests that don't require a display."""

    def test_platform_properties(self):
        from pyguit.automation.controller import GUIController, _IS_LINUX

        # Can't instantiate GUIController without display on Linux
        # but we can test the module-level constant
        if sys.platform.startswith("linux"):
            assert _IS_LINUX is True
        elif sys.platform == "win32":
            assert _IS_LINUX is False
