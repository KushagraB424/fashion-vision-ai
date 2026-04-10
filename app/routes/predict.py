"""
FastAPI routes for the fashion segmentation API.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse

from app.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    PredictionResponse,
    ShoppingLink,
)
from utils.image_utils import load_image_from_upload

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check(request: Request):
    """Check whether models are loaded and the server is ready."""
    return HealthResponse(
        status="ok",
        segmentation_model_loaded=request.app.state.seg_service is not None,
        classification_model_loaded=request.app.state.cls_service is not None,
    )


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: Request, file: UploadFile = File(...)):
    """
    Full pipeline: image → segmentation → classification.
    Shopping links are handled separately via /api/chat.
    """
    try:
        image = await load_image_from_upload(file)
    except ValueError as exc:
        return PredictionResponse(success=False, message=str(exc))

    pipeline = request.app.state.pipeline
    result = await pipeline.run(image)
    return result


@router.post("/segment", tags=["Segmentation"])
async def segment_only(request: Request, file: UploadFile = File(...)):
    """Run segmentation only and return bounding boxes + class info."""
    try:
        image = await load_image_from_upload(file)
    except ValueError as exc:
        return JSONResponse({"success": False, "error": str(exc)}, status_code=400)

    seg = request.app.state.seg_service
    objects = seg.segment(image)
    return {
        "success": True,
        "num_objects": len(objects),
        "objects": [
            {
                "class_name": o.class_name,
                "confidence": round(o.confidence, 3),
                "bbox": o.bbox,
            }
            for o in objects
        ],
    }


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: Request, body: ChatRequest):
    """
    AI Shopping Chat endpoint.

    Receives detected items, generates real shopping URLs dynamically,
    then asks the LLM to present them in a friendly conversational format.
    The LLM does NOT invent URLs — only uses the ones we provide.
    """
    agent = request.app.state.agent

    items_data = [
        {
            "label": item.label,
            "color": item.color,
            "pattern": item.pattern,
            "confidence": item.confidence,
        }
        for item in body.items
    ]

    message, links = await agent.chat(items_data, body.user_message)

    shopping_links = [ShoppingLink(**lnk) for lnk in links]

    return ChatResponse(
        success=True,
        message=message,
        shopping_links=shopping_links,
    )
