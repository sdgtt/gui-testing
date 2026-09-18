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

try:
    from pytesseract import Output
except ImportError:
    Output = None

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

    def find_text(
        self,
        image_path: str,
        target_text: str,
        threshold: int = 127,
        preprocess: str = "threshold",
        min_confidence: int = 40,
    ) -> list[dict]:
        """Find all occurrences of target text in an image.

        Returns a list of dicts with keys: text, x, y, w, h, cx, cy
        where cx/cy are the center coordinates for clicking.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")

        processed = self._preprocess(image, preprocess, threshold)
        if len(processed.shape) == 2:
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

        data = pytesseract.image_to_data(
            processed, lang=self._lang, output_type=pytesseract.Output.DICT
        )

        matches = []
        target_lower = target_text.lower()
        n = len(data["text"])

        for i in range(n):
            conf = int(data["conf"][i])
            word = data["text"][i].strip()
            if conf < min_confidence or not word:
                continue

            if target_lower in word.lower():
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                matches.append({
                    "text": word,
                    "x": x, "y": y, "w": w, "h": h,
                    "cx": x + w // 2,
                    "cy": y + h // 2,
                    "confidence": conf,
                })

        # Also try matching across adjacent words (e.g. "Signal Generator" = two words)
        if " " in target_text and not matches:
            matches = self._find_multi_word(data, target_text, min_confidence)

        return matches

    def _find_multi_word(
        self,
        data: dict,
        target_text: str,
        min_confidence: int,
    ) -> list[dict]:
        """Find multi-word text by joining adjacent OCR words on the same line."""
        target_lower = target_text.lower()
        word_count = len(target_text.split())
        n = len(data["text"])
        matches = []

        for i in range(n - word_count + 1):
            words = []
            valid = True
            for j in range(word_count):
                idx = i + j
                conf = int(data["conf"][idx])
                word = data["text"][idx].strip()
                if conf < min_confidence or not word:
                    valid = False
                    break
                if j > 0 and data["line_num"][idx] != data["line_num"][i]:
                    valid = False
                    break
                words.append(word)

            if not valid:
                continue

            joined = " ".join(words)
            if target_lower in joined.lower():
                x = data["left"][i]
                y = data["top"][i]
                last = i + word_count - 1
                right = data["left"][last] + data["width"][last]
                bottom = max(data["top"][k] + data["height"][k] for k in range(i, last + 1))
                w = right - x
                h = bottom - y
                matches.append({
                    "text": joined,
                    "x": x, "y": y, "w": w, "h": h,
                    "cx": x + w // 2,
                    "cy": y + h // 2,
                    "confidence": min(int(data["conf"][i + k]) for k in range(word_count)),
                })

        return matches

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
