import cv2
import numpy as np
from sklearn.cluster import KMeans


def rgb_to_color_name(rgb):

    r, g, b = rgb

    # white
    if r > 200 and g > 200 and b > 200:
        return "white"

    # black
    if r < 60 and g < 60 and b < 60:
        return "black"

    # gray
    if abs(r-g) < 20 and abs(r-b) < 20 and abs(g-b) < 20:
        return "gray"

    # red
    if r > 150 and g < 100 and b < 100:
        return "red"

    # green
    if g > 150 and r < 120 and b < 120:
        return "green"

    # blue
    if b > 150 and r < 120 and g < 120:
        return "blue"

    # yellow
    if r > 180 and g > 180 and b < 120:
        return "yellow"

    # brown (very common clothing color)
    if r > 120 and g > 80 and b < 80:
        return "brown"

    # beige / tan
    if r > 200 and g > 180 and b > 140:
        return "beige"

    return "unknown"


def detect_color(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w, _ = image.shape

    # focus center region
    image = image[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]

    pixels = image.reshape((-1, 3))

    pixels = pixels[np.sum(pixels, axis=1) > 60]

    if len(pixels) == 0:
        return "unknown"

    kmeans = KMeans(n_clusters=3, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_
    labels = kmeans.labels_

    counts = np.bincount(labels)
    dominant = colors[np.argmax(counts)]

    r, g, b = dominant

    return rgb_to_color_name((r, g, b))