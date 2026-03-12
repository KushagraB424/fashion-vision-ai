from ultralytics import YOLO

model = None

def load_models():
    global model
    model = YOLO("yolov8n-seg.pt")