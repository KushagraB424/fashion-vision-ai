from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

def segment(image):

    results = model(image)[0]

    detections = []

    for box in results.boxes:

        cls = int(box.cls[0])
        label = model.names[cls]

        if label != "person":
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "type": "person",
            "bbox": [x1, y1, x2, y2]
        })

    return detections