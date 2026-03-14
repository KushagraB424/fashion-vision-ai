import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_color(image):

    # resize for faster processing
    image = cv2.resize(image, (100, 100))

    pixels = image.reshape((-1, 3))

    # cluster colors
    kmeans = KMeans(n_clusters=3, n_init=10)
    kmeans.fit(pixels)

    dominant = kmeans.cluster_centers_[0]

    b, g, r = dominant

    if r > 200 and g > 200 and b > 200:
        return "white"

    if r < 60 and g < 60 and b < 60:
        return "black"

    if r > g and r > b:
        return "red"

    if b > r and b > g:
        return "blue"

    if g > r and g > b:
        return "green"

    return "unknown"