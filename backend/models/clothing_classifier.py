import cv2
import torch
import open_clip
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="laion2b_s34b_b79k"
)

model = model.to(device)

labels = [
    "t shirt",
    "shirt",
    "jacket",
    "coat",
    "hoodie",
    "sweater",
    "blazer",
    "pants",
    "trousers",
    "jeans",
    "shorts",
    "skirt",
    "dress",
    "sneakers",
    "shoes",
    "boots"
]

text_tokens = open_clip.tokenize(labels).to(device)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)


def classify_clothing(image):

    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        image = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            similarity = (100 * image_features @ text_features.T).softmax(dim=-1)

        idx = similarity.argmax().item()

        return labels[idx]

    except Exception as e:
        print("CLIP error:", e)
        return "unknown"