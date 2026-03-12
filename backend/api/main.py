from fastapi import FastAPI, UploadFile
import numpy as np
import cv2

from models.model_loader import load_models
from models.segmentation import segment_clothes

app = FastAPI()

@app.on_event("startup")
def startup():

    load_models()

@app.post("/analyze")

async def analyze(file: UploadFile):

    contents = await file.read()

    image = cv2.imdecode(
        np.frombuffer(contents,np.uint8),
        cv2.IMREAD_COLOR
    )

    items = segment_clothes(image)

    return {"items":items}