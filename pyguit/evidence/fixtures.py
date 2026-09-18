from __future__ import annotations

import pytest

from pyguit.automation.controller import GUIController
from pyguit.evidence.collector import EvidenceCollector


@pytest.fixture(scope="class")
def gui_controller():
    """Provide a GUIController instance with proper lifecycle."""
    with GUIController() as controller:
        if controller.is_linux:
            controller.attach_openbox()
        yield controller


@pytest.fixture(scope="function")
def evidence(request):
    """Provide an EvidenceCollector per test function, auto-finalizes on teardown."""
    device = request.config.getoption("--device", default="")
    collector = EvidenceCollector(
        test_name=request.node.name,
        device=device,
    )
    yield collector
    collector.finalize()
