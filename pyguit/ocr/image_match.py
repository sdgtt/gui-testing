from __future__ import annotations

import cv2
import numpy as np


def find_template(
    screenshot_path: str,
    template_path: str,
    method: int = cv2.TM_CCOEFF_NORMED,
) -> tuple[tuple[int, int], tuple[int, int], float] | None:
    """Find the best match of a template in a screenshot.

    Returns (top_left, bottom_right, confidence) or None if images can't be loaded.
    """
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)
    if screenshot is None or template is None:
        return None

    if screenshot.shape[0] < template.shape[0] or screenshot.shape[1] < template.shape[1]:
        return None

    result = cv2.matchTemplate(screenshot, template, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    bottom_right = (
        top_left[0] + template.shape[1],
        top_left[1] + template.shape[0],
    )
    return top_left, bottom_right, float(max_val)


def find_all_templates(
    screenshot_path: str,
    template_path: str,
    threshold: float = 0.8,
    method: int = cv2.TM_CCOEFF_NORMED,
) -> list[tuple[tuple[int, int], tuple[int, int], float]]:
    """Find all matches of a template above a confidence threshold."""
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)
    if screenshot is None or template is None:
        return []

    if screenshot.shape[0] < template.shape[0] or screenshot.shape[1] < template.shape[1]:
        return []

    result = cv2.matchTemplate(screenshot, template, method)
    locations = np.where(result >= threshold)
    matches = []

    th, tw = template.shape[:2]
    for pt in zip(*locations[::-1]):
        top_left = (int(pt[0]), int(pt[1]))
        bottom_right = (top_left[0] + tw, top_left[1] + th)
        confidence = float(result[pt[1], pt[0]])
        matches.append((top_left, bottom_right, confidence))

    return matches


def images_match(
    path_a: str,
    path_b: str,
    threshold: float = 0.9,
) -> bool:
    """Check if two images match above the given confidence threshold."""
    result = find_template(path_a, path_b)
    if result is None:
        return False
    _, _, confidence = result
    return confidence >= threshold
