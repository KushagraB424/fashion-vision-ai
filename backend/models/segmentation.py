from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

allowed_classes = ["person", "handbag", "tie", "backpack", "shoe"]


def segment(image):

    results = model(image)

    items = []

    for r in results:

        boxes = r.boxes

        for box in boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls)

            label = r.names[cls]

            # Skip non-clothing objects
            if label not in allowed_classes:
                continue

            items.append({
                "type": label,
                "bbox": [x1, y1, x2, y2]
            })

    return items