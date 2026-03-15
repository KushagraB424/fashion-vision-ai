from ultralytics import YOLO

# Using segmentation model
model = YOLO("yolov8n-seg.pt")

def segment(image):

    results = model(image)

    detections = []

    for r in results:

        boxes = r.boxes.xyxy.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()

        for box, cls in zip(boxes, classes):

            x1, y1, x2, y2 = map(int, box)

            label = model.names[int(cls)]

            # Only keep clothing related detections
            clothing_classes = [
                "person",
                "handbag",
                "backpack",
                "tie",
                "shoe"
            ]

            if label not in clothing_classes:
                continue

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "type": label
            })

    return detections