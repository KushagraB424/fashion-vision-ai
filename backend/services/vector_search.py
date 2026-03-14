import faiss
import numpy as np

# dimension of CLIP embeddings
dimension = 512

# FAISS index
index = faiss.IndexFlatL2(dimension)

# store product metadata
product_db = []


def add_product(embedding, metadata):

    embedding = np.array([embedding]).astype("float32")

    index.add(embedding)

    product_db.append(metadata)


def search_similar(embedding, k=3):

    embedding = np.array([embedding]).astype("float32")

    distances, indices = index.search(embedding, k)

    results = []

    for i in indices[0]:

        if i < len(product_db):
            results.append(product_db[i])

    return results