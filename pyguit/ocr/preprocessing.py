from __future__ import annotations

from typing import Any

import cv2
import numpy as np


def to_grayscale(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_threshold(image: np.ndarray, value: int = 127) -> np.ndarray:
    gray = to_grayscale(image)
    _, thresh = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    return thresh


def apply_adaptive_threshold(
    image: np.ndarray, block_size: int = 11, c: int = 2
) -> np.ndarray:
    gray = to_grayscale(image)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        block_size, c,
    )


def apply_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    gray = to_grayscale(image)
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def resize_for_ocr(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
    h, w = image.shape[:2]
    return cv2.resize(
        image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC
    )


PREPROCESS_STEPS: dict[str, Any] = {
    "grayscale": to_grayscale,
    "threshold": apply_threshold,
    "adaptive": apply_adaptive_threshold,
    "blur": apply_blur,
    "resize": resize_for_ocr,
}


def preprocess_pipeline(
    image: np.ndarray, steps: list[str]
) -> np.ndarray:
    result = image
    for step in steps:
        func = PREPROCESS_STEPS.get(step)
        if func is None:
            raise ValueError(f"Unknown preprocessing step: {step}")
        result = func(result)
    return result
