import torch
import open_clip
from PIL import Image
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

model = model.to(device)

labels = [
    "t shirt",
    "polo shirt",
    "dress shirt",
    "jacket",
    "hoodie",
    "coat",
    "jeans",
    "pants",
    "shorts",
    "skirt",
    "dress",
    "sneakers",
    "boots",
    "sandals",
]

text_tokens = open_clip.tokenize(labels).to(device)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)


def classify_clothing(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(image)

    img = preprocess(pil).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(img)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    index = similarity.argmax().item()

    return labels[index]