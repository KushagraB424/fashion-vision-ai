import numpy as np

def crop_item(image, x1, y1, x2, y2):
    """
    Crop a detected item from the image using bounding box coordinates.
    """

    height, width = image.shape[:2]

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(width, x2)
    y2 = min(height, y2)

    crop = image[y1:y2, x1:x2]

    return crop