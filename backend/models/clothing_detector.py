from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

def detect_clothing(image):

    results = model(image)[0]

    detections = []

    for box in results.boxes:

        cls = int(box.cls[0])
        label = model.names[cls]

        # skip person class
        if label == "person":
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "type": label,
            "bbox": [x1, y1, x2, y2]
        })

    return detections