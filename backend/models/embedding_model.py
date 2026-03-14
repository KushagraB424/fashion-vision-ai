import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

def get_embedding(image):

    # convert OpenCV image to PIL
    image = Image.fromarray(image[:,:,::-1])

    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image)

    embedding = embedding.cpu().numpy()[0]

    return embedding