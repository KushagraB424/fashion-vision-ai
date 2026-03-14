from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2

from backend.models.segmentation import segment
from backend.models.color_detector import detect_color
from backend.models.embedding_model import get_embedding
from backend.services.vector_search import search_similar
from backend.utils.image_utils import crop_item
from backend.scripts.load_products import load_products


app = FastAPI()

# ---- IMPORTANT: ALLOW YOUR FRONTEND ORIGIN ----
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "https://ideal-chainsaw-97xxrj4jx5xp2x646-3000.app.github.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- LOAD VECTOR DATABASE ----
@app.on_event("startup")
def startup_event():
    load_products()


@app.get("/")
def root():
    return {"message": "Fashion Vision AI backend running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    detections = segment(image)

    items = []

    for d in detections:

        x1, y1, x2, y2 = d["bbox"]

        crop = crop_item(image, x1, y1, x2, y2)

        color = detect_color(crop)

        embedding = get_embedding(crop)

        products = search_similar(embedding)

        items.append({
            "type": d["type"],
            "color": color,
            "products": products
        })

    return {"items": items}