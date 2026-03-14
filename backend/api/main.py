from fastapi import FastAPI, UploadFile
import numpy as np
import cv2

from backend.models.embedding_model import get_embedding
from backend.models.segmentation import segment
from backend.models.color_detector import detect_color
from backend.utils.image_utils import crop_item
from backend.services.vector_search import search_similar
from backend.scripts.load_products import load_products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    load_products()


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