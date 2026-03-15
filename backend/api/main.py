from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import logging

from backend.models.segmentation import segment
from backend.models.pose_detector import detect_pose
from backend.models.color_detector import detect_color
from backend.models.embedding_model import get_embedding
from backend.models.clothing_classifier import classify_clothing
from backend.services.vector_search import search_similar
from backend.utils.image_utils import crop_item
from backend.scripts.load_products import load_products

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Enable CORS (needed for Codespaces frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    logging.info("Starting backend and loading product index...")
    load_products()
    logging.info("Product index loaded.")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    logging.info("Analyze endpoint called")

    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Run person segmentation (mask + bbox)
    detections = segment(image)

    # Pose detection for body keypoints
    poses = detect_pose(image)

    expanded = []

    for d in detections:
    
        if d["type"] != "person":
            expanded.append(d)
            continue
    
        try:
            x1, y1, x2, y2 = d["bbox"]
            height = y2 - y1
    
            # safe split
            shirt_y = y1 + int(height * 0.30)
            pants_y = y1 + int(height * 0.65)
    
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
    
        except Exception as e:
            logging.warning(f"Person split failed: {e}")

    detections = expanded

    items = []

    for d in detections:

        x1, y1, x2, y2 = d["bbox"]

        crop = crop_item(image, x1, y1, x2, y2)

        if crop is None or crop.size == 0:
            continue

        # Clothing classification
        clothing_type = classify_clothing(crop)

        # Color detection
        color = detect_color(crop)

        # Embedding generation
        embedding = get_embedding(crop)

        # Vector search
        products = search_similar(embedding, clothing_type, color)

        items.append({
            "type": clothing_type,
            "color": color,
            "bbox": [x1, y1, x2, y2],
            "products": products
        })

    return {"items": items}