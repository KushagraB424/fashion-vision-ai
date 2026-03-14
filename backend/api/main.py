from fastapi import FastAPI, UploadFile
from models.embedding_model import get_embedding
import numpy as np
import cv2

from models.segmentation import segment
from models.color_detector import detect_color
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

        color = detect_color(cropped)

        embedding = get_embedding(cropped)

        results.append({
            "type": item["type"],
            "color": color,
            "embedding": embedding.tolist(),
            "bbox": item["bbox"]
        })

    return {"items": results}