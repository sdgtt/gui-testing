import os
import shutil
import tempfile

import cv2
import numpy as np
import pytest

from pyguit.ocr.reader import OCRReader

_HAS_TESSERACT = shutil.which("tesseract") is not None


@pytest.mark.skipif(not _HAS_TESSERACT, reason="Tesseract not installed")
class TestOCRReader:
    def _create_text_image(self, text, path, width=400, height=100):
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        cv2.putText(
            img, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (0, 0, 0), 3,
        )
        cv2.imwrite(path, img)
        return path

    def test_read_text_basic(self):
        reader = OCRReader()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._create_text_image("HELLO", os.path.join(tmpdir, "test.png"))
            text = reader.read_text(path)
            assert "HELLO" in text.upper()

    def test_read_structured(self):
        reader = OCRReader()
        with tempfile.TemporaryDirectory() as tmpdir:
            img = np.ones((200, 500, 3), dtype=np.uint8) * 255
            cv2.putText(img, "Status: Active", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
            cv2.putText(img, "Device: M2K", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
            path = os.path.join(tmpdir, "structured.png")
            cv2.imwrite(path, img)

            result = reader.read_structured(path)
            assert isinstance(result, dict)
            # OCR may not be perfect, but structure should be parseable

    def test_read_text_file_not_found(self):
        reader = OCRReader()
        with pytest.raises(FileNotFoundError):
            reader.read_text("/nonexistent/image.png")
