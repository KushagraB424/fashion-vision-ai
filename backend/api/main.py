from fastapi import FastAPI, UploadFile
import numpy as np
import cv2

from models.segmentation import segment
from utils.image_utils import crop_item

app = FastAPI()

@app.post("/analyze")

async def analyze(file: UploadFile):

    contents = await file.read()

    image = cv2.imdecode(
        np.frombuffer(contents,np.uint8),
        cv2.IMREAD_COLOR
    )

    detections = segment(image)

    results = []

    for item in detections:

        cropped = crop_item(image, item["bbox"])

        results.append({
            "type": item["type"],
            "bbox": item["bbox"]
        })

    return {"items": results}