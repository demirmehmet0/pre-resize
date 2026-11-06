"""
Resize math shared by the executors. Pure OpenCV/NumPy, no SDK, so it can be tested on its own.

Every function returns the new frame and the transform that maps a point of the original frame onto it:
    x_new = x * scale_x + offset_x
    y_new = y * scale_y + offset_y
Detections drawn on the original frame can be moved with it (a crop can push them partly outside).
"""

import cv2
import numpy as np


def _interpolation(src_w, src_h, dst_w, dst_h):
    # INTER_AREA keeps detail when shrinking; INTER_LINEAR is the usual choice when enlarging.
    return cv2.INTER_AREA if dst_w * dst_h < src_w * src_h else cv2.INTER_LINEAR


def hex_to_bgr(value):
    value = value.lstrip("#")
    r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    return b, g, r


def stretch(img, width, height):
    """Exactly width x height; the aspect ratio is not kept."""
    h, w = img.shape[:2]
    out = cv2.resize(img, (width, height), interpolation=_interpolation(w, h, width, height))
    return out, {"scale_x": width / w, "scale_y": height / h, "offset_x": 0.0, "offset_y": 0.0}


def fit_within(img, width, height):
    """Largest size that fits inside width x height with the aspect ratio kept; no padding."""
    h, w = img.shape[:2]
    scale = min(width / w, height / h)
    new_w, new_h = max(1, round(w * scale)), max(1, round(h * scale))
    out = cv2.resize(img, (new_w, new_h), interpolation=_interpolation(w, h, new_w, new_h))
    return out, {"scale_x": new_w / w, "scale_y": new_h / h, "offset_x": 0.0, "offset_y": 0.0}


def letterbox(img, width, height, pad_color="#000000"):
    """Fit within width x height, then pad the rest evenly with pad_color: always exactly width x height."""
    fitted, t = fit_within(img, width, height)
    new_h, new_w = fitted.shape[:2]
    left = (width - new_w) // 2
    top = (height - new_h) // 2
    color = hex_to_bgr(pad_color)
    if fitted.ndim == 2:
        color = color[0]
    out = cv2.copyMakeBorder(
        fitted, top, height - new_h - top, left, width - new_w - left, cv2.BORDER_CONSTANT, value=color
    )
    t["offset_x"], t["offset_y"] = float(left), float(top)
    return out, t


def center_crop(img, width, height):
    """Fill width x height with the aspect ratio kept, then cut the overflow from the centre."""
    h, w = img.shape[:2]
    scale = max(width / w, height / h)
    new_w, new_h = max(width, round(w * scale)), max(height, round(h * scale))
    scaled = cv2.resize(img, (new_w, new_h), interpolation=_interpolation(w, h, new_w, new_h))
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    out = np.ascontiguousarray(scaled[top : top + height, left : left + width])
    return out, {"scale_x": new_w / w, "scale_y": new_h / h, "offset_x": float(-left), "offset_y": float(-top)}
