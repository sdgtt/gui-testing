from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pyguit.evidence.metadata import TestMetadata

if TYPE_CHECKING:
    from pyguit.automation.controller import GUIController

log = logging.getLogger(__name__)


class EvidenceCollector:
    """Manages evidence directory structure and captures screenshots, logs, artifacts."""

    def __init__(
        self,
        base_dir: str = "results",
        test_name: str = "",
        device: str = "",
    ) -> None:
        self._test_name = test_name or "unnamed"
        self._base_dir = os.path.join(base_dir, self._test_name)
        self._screenshots_dir = os.path.join(self._base_dir, "screenshots")
        self._logs_dir = os.path.join(self._base_dir, "logs")
        self._artifacts_dir = os.path.join(self._base_dir, "artifacts")

        for d in (self._screenshots_dir, self._logs_dir, self._artifacts_dir):
            os.makedirs(d, exist_ok=True)

        self._metadata = TestMetadata(
            test_name=self._test_name,
            device=device,
        )

    @property
    def evidence_dir(self) -> str:
        return self._base_dir

    @property
    def screenshots_dir(self) -> str:
        return self._screenshots_dir

    @property
    def metadata(self) -> TestMetadata:
        return self._metadata

    def capture_screenshot(
        self,
        controller: GUIController,
        filename: str,
        region: tuple[int, int, int, int] | None = None,
    ) -> str:
        filepath = os.path.join(self._screenshots_dir, filename)
        controller.capture_screenshot(filepath, region=region)
        self._metadata.screenshots.append(filepath)
        return filepath

    def save_log(self, name: str, content: str) -> str:
        if not name.endswith(".log"):
            name = f"{name}.log"
        filepath = os.path.join(self._logs_dir, name)
        with open(filepath, "w") as f:
            f.write(content)
        self._metadata.logs.append(filepath)
        return filepath

    def save_artifact(self, name: str, data: bytes) -> str:
        filepath = os.path.join(self._artifacts_dir, name)
        with open(filepath, "wb") as f:
            f.write(data)
        self._metadata.artifacts.append(filepath)
        return filepath

    def set_status(self, status: str) -> None:
        self._metadata.status = status

    def add_extra(self, key: str, value: object) -> None:
        self._metadata.extra[key] = value

    def finalize(self) -> str:
        self._metadata.end_time = datetime.now(timezone.utc).isoformat()
        metadata_path = os.path.join(self._base_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            f.write(self._metadata.to_json())
        return metadata_path
