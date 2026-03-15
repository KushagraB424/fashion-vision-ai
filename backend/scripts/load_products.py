import numpy as np
from backend.services.vector_search import add_product

def load_products():

    products = [
        {
            "name": "Men White Sneakers",
            "link": "https://www.nike.com"
        },
        {
            "name": "Casual Polo Shirt",
            "link": "https://www.zara.com"
        },
        {
            "name": "Slim Fit Pants",
            "link": "https://www.hm.com"
        },
        {
            "name": "Leather Jacket",
            "link": "https://www.uniqlo.com"
        },
        {
            "name": "Running Shoes",
            "link": "https://www.adidas.com"
        },
        {
            "name": "Casual T Shirt",
            "link": "https://www.levi.com"
        },
        {
            "name": "Denim Jacket",
            "link": "https://www.gap.com"
        },
        {
            "name": "Fashion Sneakers",
            "link": "https://www.puma.com"
        },
        {
            "name": "Streetwear Hoodie",
            "link": "https://www.supreme.com"
        },
        {
            "name": "Classic White Shirt",
            "link": "https://www.uniqlo.com"
        }
    ]

    for p in products:

        embedding = np.random.rand(512)

        add_product(embedding, p)

    print("products loaded")