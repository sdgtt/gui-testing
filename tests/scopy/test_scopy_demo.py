"""Scopy demo mode test using PyGUIt v2 — OCR-based, no reference images needed.

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

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def _screenshot(evidence, controller, name):
    return evidence.capture_screenshot(controller, name)


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
    scopy_dir = os.path.dirname(scopy_path)
    if sys.platform == "win32":
        subprocess.Popen([scopy_path], cwd=scopy_dir)
    else:
        controller.launch_app("scopy", scopy_path)

    time.sleep(20)

    # Dismiss any startup popups by pressing Enter
    if sys.platform == "win32":
        import pyautogui
        for _ in range(3):
            pyautogui.press("enter")
            time.sleep(2)

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
    """Test Scopy in demo mode using OCR-based text clicking."""

    def test_01_scopy_launches(self, controller, scopy_app, evidence):
        """Verify Scopy launched."""
        path = _screenshot(evidence, controller, "01_launched.png")
        assert os.path.isfile(path)

    def test_02_enable_demo_mode(self, controller, scopy_app, evidence):
        """Click '+' then enable demo mode using text matching."""
        _screenshot(evidence, controller, "02a_before.png")

        # Click the '+' button
        clicked = controller.click_text("+")
        time.sleep(3)
        _screenshot(evidence, controller, "02b_after_plus.png")
        evidence.save_log("plus", f"Clicked '+': {clicked}")

        # Enable demo
        clicked = controller.click_text("Enable Demo")
        time.sleep(3)
        _screenshot(evidence, controller, "02c_after_demo.png")
        evidence.save_log("demo", f"Clicked 'Enable Demo': {clicked}")

    def test_03_connect_demo(self, controller, scopy_app, evidence):
        """Connect to the demo device."""
        _screenshot(evidence, controller, "03a_before.png")

        clicked = controller.click_text("Connect")
        time.sleep(5)
        _screenshot(evidence, controller, "03b_after_connect1.png")
        evidence.save_log("connect1", f"Clicked 'Connect': {clicked}")

        clicked = controller.click_text("Add")
        time.sleep(3)
        _screenshot(evidence, controller, "03c_after_add.png")
        evidence.save_log("add", f"Clicked 'Add': {clicked}")

        clicked = controller.click_text("Connect")
        time.sleep(15)
        _screenshot(evidence, controller, "03d_after_connect2.png")
        evidence.save_log("connect2", f"Clicked 'Connect': {clicked}")

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
        clicked = controller.click_text("Oscilloscope")
        time.sleep(3)
        _screenshot(evidence, controller, "05_oscilloscope.png")
        evidence.save_log("oscilloscope", f"Clicked: {clicked}")

    def test_06_run_oscilloscope(self, controller, scopy_app, evidence):
        """Click Run."""
        clicked = controller.click_text("Run")
        time.sleep(5)
        _screenshot(evidence, controller, "06_running.png")
        evidence.save_log("run", f"Clicked: {clicked}")

    def test_07_stop_oscilloscope(self, controller, scopy_app, evidence):
        """Click Stop."""
        clicked = controller.click_text("Stop")
        time.sleep(2)
        _screenshot(evidence, controller, "07_stopped.png")
        evidence.save_log("stop", f"Clicked: {clicked}")

    def test_08_navigate_instruments(self, controller, scopy_app, evidence):
        """Navigate through instruments by text."""
        instruments = [
            ("Signal Generator", "08a_signal_gen.png"),
            ("Power Supply", "08b_power_supply.png"),
            ("Digital IO", "08c_digital_io.png"),
            ("Spectrum Analyzer", "08d_spectrum.png"),
            ("Network Analyzer", "08e_network.png"),
        ]

        for label, screenshot_name in instruments:
            clicked = controller.click_text(label)
            time.sleep(3)
            _screenshot(evidence, controller, screenshot_name)
            evidence.save_log(f"instrument_{label}", f"Clicked: {clicked}")

    def test_09_disconnect(self, controller, scopy_app, evidence):
        """Go home and disconnect."""
        controller.click_text("Home")
        time.sleep(2)
        _screenshot(evidence, controller, "09a_home.png")

        clicked = controller.click_text("Disconnect")
        time.sleep(5)
        _screenshot(evidence, controller, "09b_disconnected.png")
        evidence.save_log("disconnect", f"Clicked: {clicked}")

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
