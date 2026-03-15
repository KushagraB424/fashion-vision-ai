import urllib.parse

def search_similar(embedding, item_type=None, color=None):

    if item_type is None:
        item_type = "clothing"

    if color is None:
        color = ""

    query = f"{color} {item_type}".strip()

    encoded = urllib.parse.quote(query)

    amazon = f"https://www.amazon.in/s?k={encoded}"
    myntra = f"https://www.myntra.com/{encoded.replace(' ', '-')}"
    google = f"https://www.google.com/search?tbm=shop&q={encoded}"

    products = [
        {
            "name": f"Search Amazon for {query}",
            "link": amazon
        },
        {
            "name": f"Search Myntra for {query}",
            "link": myntra
        },
        {
            "name": f"Google Shopping results for {query}",
            "link": google
        }
    ]

    return products