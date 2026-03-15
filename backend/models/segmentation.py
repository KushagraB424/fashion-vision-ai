from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8n-seg.pt")

def segment(image):

    results = model(image)

    detections = []

    for r in results:

        if r.masks is None:
            continue

        boxes = r.boxes.xyxy.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()
        masks = r.masks.xy

        for box, cls, polygon in zip(boxes, classes, masks):

            label = model.names[int(cls)]

            if label != "person":
                continue

            x1, y1, x2, y2 = map(int, box)

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "polygon": polygon.tolist(),
                "type": "person"
            })

    return detections