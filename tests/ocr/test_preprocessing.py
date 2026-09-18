import numpy as np

from pyguit.ocr.preprocessing import (
    apply_adaptive_threshold,
    apply_blur,
    apply_threshold,
    preprocess_pipeline,
    resize_for_ocr,
    to_grayscale,
)


class TestPreprocessing:
    def _make_color_image(self, w=100, h=80):
        return np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)

    def _make_gray_image(self, w=100, h=80):
        return np.random.randint(0, 255, (h, w), dtype=np.uint8)

    def test_to_grayscale_from_color(self):
        img = self._make_color_image()
        gray = to_grayscale(img)
        assert len(gray.shape) == 2
        assert gray.shape == (80, 100)

    def test_to_grayscale_already_gray(self):
        img = self._make_gray_image()
        gray = to_grayscale(img)
        assert len(gray.shape) == 2

    def test_apply_threshold(self):
        img = self._make_color_image()
        result = apply_threshold(img, 127)
        assert len(result.shape) == 2
        unique_vals = set(np.unique(result))
        assert unique_vals.issubset({0, 255})

    def test_apply_adaptive_threshold(self):
        img = self._make_color_image()
        result = apply_adaptive_threshold(img)
        assert len(result.shape) == 2

    def test_apply_blur(self):
        img = self._make_color_image()
        result = apply_blur(img)
        assert len(result.shape) == 2

    def test_resize_for_ocr(self):
        img = self._make_color_image(100, 80)
        result = resize_for_ocr(img, scale=2.0)
        assert result.shape[0] == 160
        assert result.shape[1] == 200

    def test_preprocess_pipeline(self):
        img = self._make_color_image()
        result = preprocess_pipeline(img, ["grayscale", "threshold"])
        assert len(result.shape) == 2
