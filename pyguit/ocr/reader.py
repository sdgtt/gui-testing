from __future__ import annotations

import logging
import re
import shutil

import cv2
import numpy as np
import pytesseract

from pyguit.ocr.preprocessing import (
    apply_adaptive_threshold,
    apply_blur,
    apply_threshold,
    to_grayscale,
)

log = logging.getLogger(__name__)


class OCRReader:
    """Wraps Tesseract OCR with cross-platform path detection and preprocessing."""

    def __init__(
        self, tesseract_cmd: str | None = None, lang: str = "eng"
    ) -> None:
        self._lang = lang

        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            detected = shutil.which("tesseract")
            if detected:
                pytesseract.pytesseract.tesseract_cmd = detected
            else:
                _fallbacks = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                    "/usr/bin/tesseract",
                    "/usr/local/bin/tesseract",
                ]
                import os

                for path in _fallbacks:
                    if os.path.isfile(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break

    def read_text(
        self,
        image_path: str,
        threshold: int = 127,
        preprocess: str = "threshold",
    ) -> str:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
        processed = self._preprocess(image, preprocess, threshold)
        text = pytesseract.image_to_string(processed, lang=self._lang)
        return text.strip()

    def read_structured(
        self,
        image_path: str,
        threshold: int = 127,
    ) -> dict[str, str]:
        raw_text = self.read_text(image_path, threshold)
        return self._parse_key_values(raw_text)

    def read_region(
        self,
        image_path: str,
        region: tuple[int, int, int, int],
        threshold: int = 127,
    ) -> str:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
        x, y, w, h = region
        cropped = image[y : y + h, x : x + w]
        processed = self._preprocess(cropped, "threshold", threshold)
        text = pytesseract.image_to_string(processed, lang=self._lang)
        return text.strip()

    def read_from_array(
        self,
        image: np.ndarray,
        threshold: int = 127,
        preprocess: str = "threshold",
    ) -> str:
        processed = self._preprocess(image, preprocess, threshold)
        text = pytesseract.image_to_string(processed, lang=self._lang)
        return text.strip()

    @staticmethod
    def _preprocess(
        image: np.ndarray, method: str, threshold: int
    ) -> np.ndarray:
        if method == "threshold":
            return apply_threshold(image, threshold)
        elif method == "adaptive":
            return apply_adaptive_threshold(image)
        elif method == "blur":
            return apply_blur(image)
        elif method == "none":
            return to_grayscale(image)
        return apply_threshold(image, threshold)

    @staticmethod
    def _parse_key_values(text: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            match = re.match(r"^([^:]+):\s*(.+)$", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                result[key] = value
        return result
