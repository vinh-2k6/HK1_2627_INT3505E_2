from flask.views import MethodView
from flask_smorest import Blueprint

from schemas.products import ProductSchema, ProductInSchema

blp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    description="Product API"
)

# Database
products = [
    {"id": 1, "name": "Laptop", "price": 1500},
    {"id": 2, "name": "Mouse", "price": 25}
]


@blp.route("/")
class ProductList(MethodView):

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return products

    @blp.arguments(ProductInSchema)
    @blp.response(201, ProductSchema)
    def post(self, data):
        new_product = {
            "id": len(products) + 1,
            "name": data["name"],
            "price": data["price"]
        }

        products.append(new_product)

        return new_product
