from __future__ import annotations

import logging
import subprocess
import sys
import threading
import time
from typing import IO

from pyguit.automation.exceptions import (
    PlatformNotSupportedError,
    ProcessNotFoundError,
)

log = logging.getLogger(__name__)

_IS_LINUX = sys.platform.startswith("linux")


class ProcessManager:
    """Manages subprocess lifecycle for launched applications."""

    def __init__(self) -> None:
        self._processes: dict[str, subprocess.Popen] = {}

    def run(
        self,
        name: str,
        command: list[str],
        daemon: bool = False,
        log_dir: str | None = None,
    ) -> subprocess.Popen:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self._processes[name] = process

        def _drain(proc: subprocess.Popen) -> None:
            stdout, stderr = proc.communicate()
            if log_dir:
                _write_safe(f"{log_dir}/{name}.log", stdout or "")
                _write_safe(f"{log_dir}/{name}_err.log", stderr or "")

        thread = threading.Thread(target=_drain, args=(process,), daemon=daemon)
        thread.start()
        return process

    def stop(self, name: str, timeout: float = 5.0) -> None:
        process = self._processes.pop(name, None)
        if process is None:
            raise ProcessNotFoundError(f"No process named '{name}'")
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)

    def launch_app(
        self,
        app_name: str,
        path: str,
        *,
        host: str | None = None,
        user: str | None = None,
        daemon: bool = True,
    ) -> subprocess.Popen:
        if host:
            command = ["ssh", "-X", f"{user}@{host}", path]
        else:
            command = [path]
        return self.run(app_name, command, daemon=daemon)

    def attach_openbox(self) -> None:
        if not _IS_LINUX:
            raise PlatformNotSupportedError(
                "Openbox window manager is only available on Linux"
            )
        self.run("openbox", ["openbox-session"], daemon=True)

    def detach_openbox(self) -> None:
        self.stop("openbox")

    def stop_all(self) -> None:
        for name in list(self._processes):
            try:
                self.stop(name)
            except ProcessNotFoundError:
                pass

    def is_running(self, name: str) -> bool:
        proc = self._processes.get(name)
        return proc is not None and proc.poll() is None


def _write_safe(path: str, content: str) -> None:
    try:
        with open(path, "w") as f:
            f.write(content)
    except OSError:
        log.warning("Could not write log to %s", path)
