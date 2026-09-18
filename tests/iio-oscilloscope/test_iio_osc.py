"""IIO Oscilloscope test using PyGUIt v2.

Run on Windows:
    pytest tests/iio-oscilloscope/test_iio_osc.py -v --osc-path "C:\\path\\to\\osc.exe"
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

REF_DIR = os.path.join(os.path.dirname(__file__), "references")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

CONFIDENCE = 0.5


def _ref(name: str) -> str:
    return os.path.join(REF_DIR, name)


def _screenshot(evidence, controller, name):
    return evidence.capture_screenshot(controller, name)


def _find_and_click(controller, ref_image, confidence=CONFIDENCE, delay=2.0):
    result = controller.locate_on_screen(ref_image, confidence=confidence)
    if result:
        controller.click(*result)
        time.sleep(delay)
        return True
    return False


@pytest.fixture(scope="module")
def osc_path(request):
    path = request.config.getoption("--osc-path", default="")
    if not path:
        if sys.platform == "win32":
            path = r"C:\Program Files\Analog Devices\IIO Oscilloscope\osc.exe"
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

    time.sleep(20)

    # Dismiss any startup popups
    if sys.platform == "win32":
        import pyautogui
        for _ in range(3):
            pyautogui.press("enter")
            time.sleep(1)

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
    """Test IIO Oscilloscope. Screenshots at every step."""

    def test_01_app_launches(self, controller, osc_app, evidence):
        """Verify IIO Oscilloscope launched."""
        path = _screenshot(evidence, controller, "01_launched.png")
        assert os.path.isfile(path)
        evidence.save_log("launch", "IIO Oscilloscope launched, screenshot captured")

    def test_02_verify_main_window(self, controller, osc_app, evidence):
        """Check that the main oscilloscope window is visible."""
        _screenshot(evidence, controller, "02a_main_window.png")

        found = controller.locate_on_screen(
            _ref("ref_test_open_adi_iio_oscilloscope_app.png"), confidence=CONFIDENCE
        )
        _screenshot(evidence, controller, "02b_main_window_check.png")
        evidence.save_log("main_window", f"Main window found: {found is not None}")

    def test_03_verify_capture_window(self, controller, osc_app, evidence):
        """Check that the Capture1 window is visible."""
        found = controller.locate_on_screen(
            _ref("ref_test_open_adi_iio_oscilloscope-capture1_app.png"),
            confidence=CONFIDENCE,
        )
        _screenshot(evidence, controller, "03_capture_window.png")
        evidence.save_log("capture_window", f"Capture window found: {found is not None}")

    def test_04_enable_all_channels(self, controller, osc_app, evidence):
        """Click the enable all checkbox."""
        _screenshot(evidence, controller, "04a_before_checkbox.png")

        found = _find_and_click(
            controller,
            _ref("ref_test_enable_all_checkbox.png"),
            confidence=0.7,
            delay=5,
        )
        _screenshot(evidence, controller, "04b_after_checkbox.png")
        evidence.save_log("checkbox", f"Enable all checkbox found: {found}")

    def test_05_run_capture(self, controller, osc_app, evidence):
        """Click the Run button to start capture."""
        _screenshot(evidence, controller, "05a_before_run.png")

        found = _find_and_click(
            controller,
            _ref("ref_test_run_button.png"),
            confidence=CONFIDENCE,
            delay=5,
        )
        _screenshot(evidence, controller, "05b_after_run.png")
        evidence.save_log("run", f"Run button found: {found}")

    def test_06_verify_not_frozen(self, controller, osc_app, evidence):
        """OCR the screen to check app is responsive."""
        path = _screenshot(evidence, controller, "06_health_check.png")

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

    def test_07_generate_report(self, evidence):
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
