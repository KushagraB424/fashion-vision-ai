import cv2
import numpy as np
from fashion_clip.fashion_clip import FashionCLIP
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
fclip = FashionCLIP("fashion-clip")

labels = [
    "t-shirt",
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

# encode label embeddings
text_embeddings = fclip.encode_text(labels, batch_size=32)


def classify_clothing(image):

    try:
        # BGR → RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # resize for CLIP
        image = cv2.resize(image, (224, 224))

        # image embedding
        image_embedding = fclip.encode_images([image], batch_size=1)

        # cosine similarity
        sims = cosine_similarity(image_embedding, text_embeddings)

        idx = np.argmax(sims)

        return labels[idx]

    except Exception as e:
        print("FashionCLIP error:", e)
        return "unknown"