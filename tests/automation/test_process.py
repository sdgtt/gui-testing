import sys

import pytest

from pyguit.automation.exceptions import ProcessNotFoundError
from pyguit.automation.process import ProcessManager


class TestProcessManager:
    def test_run_and_stop(self):
        pm = ProcessManager()
        pm.run("sleeper", [sys.executable, "-c", "import time; time.sleep(60)"])
        assert pm.is_running("sleeper")
        pm.stop("sleeper")
        assert not pm.is_running("sleeper")

    def test_stop_unknown_raises(self):
        pm = ProcessManager()
        with pytest.raises(ProcessNotFoundError):
            pm.stop("nonexistent")

    def test_stop_all(self):
        pm = ProcessManager()
        pm.run("a", [sys.executable, "-c", "import time; time.sleep(60)"])
        pm.run("b", [sys.executable, "-c", "import time; time.sleep(60)"])
        assert pm.is_running("a")
        assert pm.is_running("b")
        pm.stop_all()
        assert not pm.is_running("a")
        assert not pm.is_running("b")

    def test_run_with_quick_exit(self):
        pm = ProcessManager()
        pm.run("quick", [sys.executable, "-c", "print('hello')"])
        import time
        time.sleep(0.5)
        assert not pm.is_running("quick")
        pm.stop_all()
