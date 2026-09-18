from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyguit.automation.controller import GUIController
    from pyguit.ocr.reader import OCRReader


def assert_text_visible(
    controller: GUIController,
    ocr_reader: OCRReader,
    expected_text: str,
    screenshot_path: str | None = None,
) -> None:
    """Assert that expected text is visible on screen via OCR."""
    if screenshot_path is None:
        import tempfile
        import os

        screenshot_path = os.path.join(
            tempfile.gettempdir(), "_pyguit_assert.png"
        )
        controller.capture_screenshot(screenshot_path)

    text = ocr_reader.read_text(screenshot_path)
    assert expected_text.lower() in text.lower(), (
        f"Expected text '{expected_text}' not found in screen OCR output"
    )


def assert_image_matches(
    controller: GUIController,
    reference_path: str,
    confidence: float = 0.9,
) -> None:
    """Assert that a reference image is visible on screen."""
    result = controller.locate_on_screen(
        reference_path, confidence=confidence
    )
    assert result is not None, (
        f"Reference image '{reference_path}' not found on screen "
        f"(confidence={confidence})"
    )


def assert_state_matches(
    observed: dict[str, str],
    expected: dict[str, str],
    tolerance: float = 0.0,
) -> None:
    """Assert observed state dict matches expected state dict."""
    mismatches = []
    for key, expected_val in expected.items():
        observed_val = observed.get(key, "")
        if tolerance and _is_numeric(expected_val) and _is_numeric(observed_val):
            if abs(float(observed_val) - float(expected_val)) > tolerance:
                mismatches.append(
                    f"  {key}: expected={expected_val} ± {tolerance}, "
                    f"observed={observed_val}"
                )
        elif observed_val.lower() != expected_val.lower():
            mismatches.append(
                f"  {key}: expected='{expected_val}', observed='{observed_val}'"
            )

    if mismatches:
        raise AssertionError(
            "State mismatch:\n" + "\n".join(mismatches)
        )


def _is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
