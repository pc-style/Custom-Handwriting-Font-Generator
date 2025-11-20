import logging
import cv2
import numpy as np
from pathlib import Path
import reflex as rx


def analyze_image_style(image_path: Path) -> dict:
    """Analyze a handwriting sample to extract style features."""
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"thickness": 5.0, "slant": 0.0, "baseline": 0}
        _, thresh = cv2.threshold(
            img, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
        valid_dist = dist[dist > 0]
        if len(valid_dist) > 0:
            top_dist = np.percentile(valid_dist, 80)
            thickness = float(top_dist * 2)
        else:
            thickness = 5.0
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        angles = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 50:
                try:
                    if len(cnt) >= 5:
                        _, _, angle = cv2.fitEllipse(cnt)
                        if angle > 90:
                            angle -= 180
                        angles.append(angle)
                except Exception as e:
                    logging.exception(f"Error fitting ellipse: {e}")
        slant = float(np.median(angles)) if angles else 0.0
        h_proj = np.sum(thresh, axis=1)
        if len(h_proj) > 0:
            y_coords = np.where(h_proj > np.max(h_proj) * 0.1)[0]
            if len(y_coords) > 0:
                baseline = int(np.percentile(y_coords, 75))
            else:
                baseline = img.shape[0] // 2
        else:
            baseline = img.shape[0] // 2
        return {
            "thickness": round(thickness, 2),
            "slant": round(slant, 2),
            "baseline": baseline,
            "height": img.shape[0],
        }
    except Exception as e:
        logging.exception(f"Error analyzing image: {e}")
        return {"thickness": 5.0, "slant": 0.0, "baseline": 0}