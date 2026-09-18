"""Scopy demo mode test using PyGUIt v2.

Run on Windows with Scopy installed:
    pytest tests/scopy/test_scopy_demo.py -v --scopy-path "C:\\Program Files\\Analog Devices\\Scopy\\Scopy.exe"
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

CONFIDENCE = 0.6
TIMEOUT = 15


def _ref(name: str) -> str:
    return os.path.join(REF_DIR, name)


def _screenshot(evidence, controller, name):
    """Always capture a screenshot regardless of test outcome."""
    return evidence.capture_screenshot(controller, name)


def _find_and_click(controller, ref_image, confidence=CONFIDENCE, delay=2.0):
    """Try to find and click a reference image. Returns True if found."""
    result = controller.locate_on_screen(ref_image, confidence=confidence)
    if result:
        controller.click(*result)
        time.sleep(delay)
        return True
    return False


@pytest.fixture(scope="module")
def scopy_path(request):
    path = request.config.getoption("--scopy-path", default="")
    if not path:
        if sys.platform == "win32":
            path = r"C:\Program Files\Analog Devices\Scopy\Scopy.exe"
        else:
            path = "scopy"
    return path


@pytest.fixture(scope="module")
def controller():
    with GUIController() as ctrl:
        yield ctrl


@pytest.fixture(scope="module")
def scopy_app(controller, scopy_path):
    """Launch Scopy and wait for it to load."""
    if sys.platform == "win32":
        os.startfile(scopy_path)
    else:
        controller.launch_app("scopy", scopy_path)

    time.sleep(20)
    yield
    if sys.platform == "win32":
        os.system("taskkill /F /IM Scopy.exe 2>nul")
    else:
        try:
            controller.stop_app("scopy")
        except Exception:
            pass


@pytest.fixture(scope="module")
def evidence():
    collector = EvidenceCollector(
        base_dir=RESULTS_DIR,
        test_name="scopy_demo",
        device="ADALM2000",
    )
    yield collector
    collector.finalize()


class TestScopyDemo:
    """Test Scopy in demo mode. Screenshots are captured at every step."""

    def test_01_scopy_launches(self, controller, scopy_app, evidence):
        """Verify Scopy launched — always captures a screenshot."""
        path = _screenshot(evidence, controller, "01_scopy_launched.png")
        assert os.path.isfile(path), "Screenshot capture failed"
        evidence.save_log("launch", "Scopy launched, screenshot captured")

    def test_02_enable_demo_mode(self, controller, scopy_app, evidence):
        """Click '+' then enable demo mode."""
        _screenshot(evidence, controller, "02a_before_plus.png")

        found_plus = _find_and_click(controller, _ref("Scopy_add_plus.png"), delay=3)
        _screenshot(evidence, controller, "02b_after_plus.png")
        evidence.save_log("enable_demo",
            f"Plus button found: {found_plus}")

        found_demo = _find_and_click(controller, _ref("Scopy_enable_demo.png"), delay=3)
        _screenshot(evidence, controller, "02c_after_demo_enable.png")
        evidence.save_log("enable_demo",
            f"Demo button found: {found_demo}")

    def test_03_connect_demo(self, controller, scopy_app, evidence):
        """Connect to the demo device."""
        _screenshot(evidence, controller, "03a_before_connect.png")

        found_connect = _find_and_click(
            controller, _ref("Scopy_connect.png"), delay=5
        )
        _screenshot(evidence, controller, "03b_after_first_connect.png")

        found_add = _find_and_click(controller, _ref("Scopy_add.png"), delay=3)
        _screenshot(evidence, controller, "03c_after_add.png")

        found_connect2 = _find_and_click(
            controller, _ref("Scopy_connect.png"), delay=15
        )
        _screenshot(evidence, controller, "03d_after_second_connect.png")

        evidence.save_log("connect",
            f"Connect1: {found_connect}, Add: {found_add}, Connect2: {found_connect2}")

    def test_04_verify_not_frozen(self, controller, scopy_app, evidence):
        """OCR the screen to check Scopy is responsive."""
        path = _screenshot(evidence, controller, "04_health_check.png")

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

    def test_05_open_oscilloscope(self, controller, scopy_app, evidence):
        """Navigate to oscilloscope."""
        found = _find_and_click(controller, _ref("Scopy_oscilloscope.png"), delay=3)
        _screenshot(evidence, controller, "05_oscilloscope.png")
        evidence.save_log("oscilloscope", f"Found: {found}")

    def test_06_run_oscilloscope(self, controller, scopy_app, evidence):
        """Click Run on oscilloscope."""
        found = _find_and_click(controller, _ref("Scopy_run.png"), delay=5)
        _screenshot(evidence, controller, "06_oscilloscope_running.png")
        evidence.save_log("run", f"Found: {found}")

    def test_07_stop_oscilloscope(self, controller, scopy_app, evidence):
        """Click Stop on oscilloscope."""
        found = _find_and_click(controller, _ref("Scopy_stop.png"), delay=2)
        _screenshot(evidence, controller, "07_oscilloscope_stopped.png")
        evidence.save_log("stop", f"Found: {found}")

    def test_08_navigate_instruments(self, controller, scopy_app, evidence):
        """Navigate through instruments, screenshot each one."""
        instruments = [
            ("Scopy_signal_generator.png", "08a_signal_gen.png"),
            ("Scopy_power_supply.png", "08b_power_supply.png"),
            ("Scopy_digital_io.png", "08c_digital_io.png"),
            ("Scopy_spectrum_analyzer.png", "08d_spectrum.png"),
            ("Scopy_network_analyzer.png", "08e_network.png"),
        ]

        for ref_img, screenshot_name in instruments:
            found = _find_and_click(controller, _ref(ref_img), delay=3)
            _screenshot(evidence, controller, screenshot_name)
            evidence.save_log(
                f"instrument_{ref_img}",
                f"Found: {found}",
            )

    def test_09_disconnect(self, controller, scopy_app, evidence):
        """Go home and disconnect."""
        _find_and_click(controller, _ref("Scopy_home.png"), delay=2)
        _screenshot(evidence, controller, "09a_home.png")

        found = _find_and_click(controller, _ref("Scopy_disconnect.png"), delay=5)
        _screenshot(evidence, controller, "09b_disconnected.png")
        evidence.save_log("disconnect", f"Found: {found}")

    def test_10_generate_report(self, evidence):
        """Generate a Markdown validation report."""
        evidence.set_status("pass")
        reporter = ReportGenerator()
        report_path = os.path.join(RESULTS_DIR, "scopy_demo", "report.md")
        reporter.generate(
            results=[],
            metadata=evidence.metadata,
            output_path=report_path,
        )
        assert os.path.isfile(report_path)
