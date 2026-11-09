products = [
    {"id": 1, "name": "Laptop", "price": 1500},
    {"id": 2, "name": "Mouse", "price": 25}
]


def list_products():
    return products, 200


def create_product(body):
    new_product = {
        "id": len(products) + 1,
        "name": body["name"],
        "price": body["price"]
    }

    products.append(new_product)

    return new_product, 201
