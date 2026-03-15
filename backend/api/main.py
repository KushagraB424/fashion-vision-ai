from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import logging

from backend.models.segmentation import segment
from backend.models.color_detector import detect_color
from backend.models.clothing_classifier import classify_clothing
from backend.utils.image_utils import crop_item

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    logging.info("Analyze endpoint called")

    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Step 1 — Person segmentation
    detections = segment(image)

    expanded = []

    # Step 2 — Split person into clothing regions
    for d in detections:

        if d["type"] != "person":
            continue

        x1, y1, x2, y2 = d["bbox"]

        height = y2 - y1

        shirt_y = y1 + int(height * 0.32)
        pants_y = y1 + int(height * 0.68)

        expanded.append({
            "bbox": [x1, y1, x2, shirt_y],
            "type": "shirt"
        })

        expanded.append({
            "bbox": [x1, shirt_y, x2, pants_y],
            "type": "pants"
        })

        expanded.append({
            "bbox": [x1, pants_y, x2, y2],
            "type": "shoes"
        })

    items = []

    # Step 3 — Process each clothing region
    for d in expanded:

        x1, y1, x2, y2 = d["bbox"]

        crop = crop_item(image, x1, y1, x2, y2)

        if crop.size == 0:
            continue

        color = detect_color(crop)

        clothing_type = classify_clothing(crop)

        items.append({
            "type": clothing_type,
            "color": color,
            "bbox": [x1, y1, x2, y2]
        })

    return {"items": items}