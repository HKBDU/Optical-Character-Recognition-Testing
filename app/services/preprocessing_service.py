import cv2
import numpy as np

def variants(image: np.ndarray) -> list[np.ndarray]:
    if image is None or image.size == 0:
        return []
    original = image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 7, 7, 21)
    return [original, cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)]

