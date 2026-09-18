import os
import tempfile

import cv2
import numpy as np

from pyguit.ocr.image_match import find_template, images_match


class TestImageMatch:
    def _write_image(self, path, image):
        cv2.imwrite(path, image)

    def test_find_template_identical(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img = np.zeros((200, 300, 3), dtype=np.uint8)
            cv2.rectangle(img, (50, 50), (100, 100), (255, 255, 255), -1)

            full_path = os.path.join(tmpdir, "full.png")
            template_path = os.path.join(tmpdir, "template.png")
            self._write_image(full_path, img)
            self._write_image(template_path, img[50:100, 50:100])

            result = find_template(full_path, template_path)
            assert result is not None
            top_left, bottom_right, confidence = result
            assert confidence > 0.9

    def test_images_match_same_image(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img = np.ones((100, 100, 3), dtype=np.uint8) * 128
            path = os.path.join(tmpdir, "img.png")
            self._write_image(path, img)
            assert images_match(path, path, threshold=0.99)

    def test_find_template_returns_none_for_missing(self):
        result = find_template("/nonexistent/a.png", "/nonexistent/b.png")
        assert result is None
