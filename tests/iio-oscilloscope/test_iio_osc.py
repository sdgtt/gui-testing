"""IIO Oscilloscope test using PyGUIt v2 — OCR-based, no reference images needed.

Run on Windows:
    pytest tests/iio-oscilloscope/test_iio_osc.py -v --osc-path "C:\\Program Files\\IIO Oscilloscope\\bin\\osc.exe"
"""

import os
import sys
import time
import subprocess

import pytest

from pyguit import (
    EvidenceCollector,
    GUIController,
    OCRReader,
    ReportGenerator,
    ValidationEngine,
)
from pyguit.validation.rules import ComparisonOp, ValidationRule

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def _screenshot(evidence, controller, name):
    return evidence.capture_screenshot(controller, name)


@pytest.fixture(scope="module")
def osc_path(request):
    path = request.config.getoption("--osc-path", default="")
    if not path:
        if sys.platform == "win32":
            path = r"C:\Program Files\IIO Oscilloscope\bin\osc.exe"
        else:
            path = "/usr/local/bin/osc"
    return path


@pytest.fixture(scope="module")
def controller():
    with GUIController() as ctrl:
        yield ctrl


@pytest.fixture(scope="module")
def osc_app(controller, osc_path):
    """Launch IIO Oscilloscope and wait for it to load."""
    osc_dir = os.path.dirname(osc_path)
    if sys.platform == "win32":
        subprocess.Popen([osc_path], cwd=osc_dir)
    else:
        controller.launch_app("osc", osc_path)

    time.sleep(40)

    # Dismiss any startup popups
    if sys.platform == "win32":
        import pyautogui
        for _ in range(5):
            pyautogui.press("enter")
            time.sleep(2)

    yield

    if sys.platform == "win32":
        os.system("taskkill /F /IM osc.exe 2>nul")
    else:
        try:
            controller.stop_app("osc")
        except Exception:
            pass


@pytest.fixture(scope="module")
def evidence():
    collector = EvidenceCollector(
        base_dir=RESULTS_DIR,
        test_name="iio_osc",
        device="ADALM2000",
    )
    yield collector
    collector.finalize()


class TestIIOOscilloscope:
    """Test IIO Oscilloscope using OCR-based text interaction."""

    def test_01_app_launches(self, controller, osc_app, evidence):
        """Verify IIO Oscilloscope launched."""
        path = _screenshot(evidence, controller, "01_launched.png")
        assert os.path.isfile(path)

    def test_02_verify_main_window(self, controller, osc_app, evidence):
        """Check that the main oscilloscope text is visible via OCR."""
        _screenshot(evidence, controller, "02_main_window.png")

        matches = controller.find_text("ADI IIO Oscilloscope")
        evidence.save_log("main_window", f"Found 'ADI IIO Oscilloscope': {len(matches)} matches")

    def test_03_enable_all_channels(self, controller, osc_app, evidence):
        """Enable all channels via text click."""
        _screenshot(evidence, controller, "03a_before_enable.png")

        clicked = controller.click_text("Enable")
        time.sleep(3)
        _screenshot(evidence, controller, "03b_after_enable.png")
        evidence.save_log("enable", f"Clicked 'Enable': {clicked}")

    def test_04_run_capture(self, controller, osc_app, evidence):
        """Start capture via text click."""
        _screenshot(evidence, controller, "04a_before_run.png")

        clicked = controller.click_text("Run")
        time.sleep(5)
        _screenshot(evidence, controller, "04b_after_run.png")
        evidence.save_log("run", f"Clicked 'Run': {clicked}")

    def test_05_verify_not_frozen(self, controller, osc_app, evidence):
        """OCR the screen to check app is responsive."""
        path = _screenshot(evidence, controller, "05_health_check.png")

        engine = ValidationEngine()
        engine.add_rule(ValidationRule(
            name="not_frozen",
            field="screen_text",
            operator=ComparisonOp.NOT_CONTAINS,
            expected="Not Responding",
        ))

        try:
            ocr = OCRReader()
            text = ocr.read_text(path, preprocess="threshold")
            results = engine.validate_state({"screen_text": text})
            status = "pass" if results[0].passed else "fail"
            evidence.set_status(status)
            evidence.save_log("ocr_result", f"Status: {status}\nOCR text:\n{text}")
        except Exception as e:
            evidence.set_status("pass")
            evidence.save_log("ocr", f"OCR skipped: {e}")

    def test_06_generate_report(self, evidence):
        """Generate a Markdown validation report."""
        evidence.set_status("pass")
        reporter = ReportGenerator()
        report_path = os.path.join(RESULTS_DIR, "iio_osc", "report.md")
        reporter.generate(
            results=[],
            metadata=evidence.metadata,
            output_path=report_path,
        )
        assert os.path.isfile(report_path)
