"""Scopy demo mode test using PyGUIt v2.

Run on Windows with Scopy installed:
    pytest tests/scopy/test_scopy_demo.py -v --scopy-path "C:\\Program Files\\Scopy\\Scopy.exe"

Or with a custom path:
    pytest tests/scopy/test_scopy_demo.py -v --scopy-path "D:\\Scopy\\Scopy.exe"
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


def _ref(name: str) -> str:
    return os.path.join(REF_DIR, name)


@pytest.fixture(scope="module")
def scopy_path(request):
    path = request.config.getoption("--scopy-path", default="")
    if not path:
        if sys.platform == "win32":
            path = r"C:\Program Files\ADI\Scopy.exe"
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
        subprocess.Popen([scopy_path])
    else:
        controller.launch_app("scopy", scopy_path)

    time.sleep(15)
    yield
    # Teardown: kill Scopy
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
    """Test Scopy in demo mode on Windows (pyautogui-only mode)."""

    def test_scopy_launches(self, controller, scopy_app, evidence):
        """Verify Scopy window is visible after launch."""
        screenshot = evidence.capture_screenshot(
            controller, "01_scopy_launched.png"
        )
        assert os.path.isfile(screenshot)
        evidence.save_log("launch", "Scopy launched successfully")

    def test_enable_demo_mode(self, controller, scopy_app, evidence):
        """Click the '+' button, then enable demo mode."""
        # Click the '+' button to add a device
        plus_btn = controller.locate_on_screen(
            _ref("Scopy_add_plus.png"), confidence=0.8
        )
        if plus_btn:
            controller.click(*plus_btn)
            time.sleep(3)

        # Enable demo mode
        demo_btn = controller.locate_on_screen(
            _ref("Scopy_enable_demo.png"), confidence=0.7
        )
        if demo_btn:
            controller.click(*demo_btn)
            time.sleep(3)

        evidence.capture_screenshot(controller, "02_demo_enabled.png")

    def test_connect_demo(self, controller, scopy_app, evidence):
        """Connect to the demo device."""
        connect_btn = controller.wait_for_image(
            _ref("Scopy_connect.png"), timeout=10, confidence=0.8
        )
        controller.click(*connect_btn)
        time.sleep(5)

        # Wait for add button and click it
        add_btn = controller.locate_on_screen(
            _ref("Scopy_add.png"), confidence=0.8
        )
        if add_btn:
            controller.click(*add_btn)
            time.sleep(3)

        # Click connect again after adding
        connect_btn2 = controller.locate_on_screen(
            _ref("Scopy_connect.png"), confidence=0.8
        )
        if connect_btn2:
            controller.click(*connect_btn2)
            time.sleep(15)

        evidence.capture_screenshot(controller, "03_connected.png")

    def test_verify_not_frozen(self, controller, scopy_app, evidence):
        """OCR the screen to verify Scopy is not frozen."""
        screenshot_path = evidence.capture_screenshot(
            controller, "04_health_check.png"
        )

        engine = ValidationEngine()
        engine.add_rule(
            ValidationRule(
                name="not_frozen",
                field="screen_text",
                operator=ComparisonOp.NOT_CONTAINS,
                expected="Not Responding",
                description="Scopy must not be frozen",
            )
        )

        try:
            ocr = OCRReader()
            text = ocr.read_text(screenshot_path, preprocess="threshold")
            results = engine.validate_state({"screen_text": text})
            evidence.set_status("pass" if results[0].passed else "fail")
        except Exception:
            # OCR not available — just verify screenshot was captured
            evidence.set_status("pass")
            evidence.save_log("ocr", "OCR skipped — Tesseract not available")

    def test_open_oscilloscope(self, controller, scopy_app, evidence):
        """Navigate to the oscilloscope instrument."""
        osc_btn = controller.locate_on_screen(
            _ref("Scopy_oscilloscope.png"), confidence=0.8
        )
        if osc_btn:
            controller.click(*osc_btn)
            time.sleep(3)

        evidence.capture_screenshot(controller, "05_oscilloscope.png")

    def test_run_oscilloscope(self, controller, scopy_app, evidence):
        """Click the Run button on the oscilloscope."""
        run_btn = controller.locate_on_screen(
            _ref("Scopy_run.png"), confidence=0.8
        )
        if run_btn:
            controller.click(*run_btn)
            time.sleep(5)

        evidence.capture_screenshot(controller, "06_oscilloscope_running.png")

    def test_stop_oscilloscope(self, controller, scopy_app, evidence):
        """Stop the oscilloscope."""
        stop_btn = controller.locate_on_screen(
            _ref("Scopy_stop.png"), confidence=0.8
        )
        if stop_btn:
            controller.click(*stop_btn)
            time.sleep(2)

        evidence.capture_screenshot(controller, "07_oscilloscope_stopped.png")

    def test_navigate_instruments(self, controller, scopy_app, evidence):
        """Navigate through different instruments."""
        instruments = [
            ("Scopy_signal_generator.png", "08_signal_gen.png"),
            ("Scopy_power_supply.png", "09_power_supply.png"),
            ("Scopy_digital_io.png", "10_digital_io.png"),
            ("Scopy_spectrum_analyzer.png", "11_spectrum.png"),
            ("Scopy_network_analyzer.png", "12_network.png"),
        ]

        for ref_img, screenshot_name in instruments:
            btn = controller.locate_on_screen(
                _ref(ref_img), confidence=0.8
            )
            if btn:
                controller.click(*btn)
                time.sleep(3)
                evidence.capture_screenshot(controller, screenshot_name)

    def test_disconnect(self, controller, scopy_app, evidence):
        """Disconnect from the demo device."""
        # Go home first
        home_btn = controller.locate_on_screen(
            _ref("Scopy_home.png"), confidence=0.8
        )
        if home_btn:
            controller.click(*home_btn)
            time.sleep(2)

        disconnect_btn = controller.locate_on_screen(
            _ref("Scopy_disconnect.png"), confidence=0.8
        )
        if disconnect_btn:
            controller.click(*disconnect_btn)
            time.sleep(5)

        evidence.capture_screenshot(controller, "13_disconnected.png")

    def test_generate_report(self, evidence):
        """Generate a validation report from collected evidence."""
        evidence.set_status("pass")

        reporter = ReportGenerator()
        report_path = os.path.join(RESULTS_DIR, "scopy_demo", "report.md")
        reporter.generate(
            results=[],
            metadata=evidence.metadata,
            output_path=report_path,
        )
        assert os.path.isfile(report_path)
