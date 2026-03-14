import numpy as np
from backend.services.vector_search import add_product

def load_products():

    for i in range(10):

        embedding = np.random.rand(512)

        metadata = {
            "name": f"product_{i}",
            "link": f"https://store.com/product_{i}"
        }

        add_product(embedding, metadata)

    print("products loaded")