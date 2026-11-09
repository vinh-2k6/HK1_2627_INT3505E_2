from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from src.extensions import db
from src.models import Product
from src.schemas.products import (
    ProductSchema,
    ProductInSchema,
    ProductPatchSchema,
    ProductReserveSchema,
    ProductListSchema,
    PaginationSchema,
)

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/api/v1/products",
    description="Operations on products",
)


@blp.route("")
@blp.route("/")
class ProductsList(MethodView):
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, pagination_data):
        page = pagination_data.get("page", 1)
        per_page = pagination_data.get("size") or pagination_data.get("per_page", 20)

        query = (
            db.select(Product)
            .where(Product.is_archived.is_(False))
            .order_by(Product.id)
        )
        pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "size": pagination.per_page,
            "per_page": pagination.per_page,
        }

    @blp.arguments(ProductInSchema, location="json")
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        existing = db.session.scalar(
            db.select(Product).where(Product.sku == product_data["sku"])
        )
        if existing:
            abort(409, message="SKU already exists.")

        product = Product(**product_data)
        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="SKU already exists.")

        return product


@blp.route("/<int:product_id>")
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = db.session.scalar(
            db.select(Product).where(
                Product.id == product_id,
                Product.is_archived.is_(False),
            )
        )
        if product is None:
            abort(404, message="Product not found.")
        return product

    @blp.arguments(ProductPatchSchema, location="json")
    @blp.response(200, ProductSchema)
    def patch(self, product_data, product_id):
        product = db.session.scalar(
            db.select(Product).where(
                Product.id == product_id,
                Product.is_archived.is_(False),
            )
        )
        if product is None:
            abort(404, message="Product not found.")

        if "sku" in product_data:
            existing = db.session.scalar(
                db.select(Product).where(
                    Product.sku == product_data["sku"],
                    Product.id != product_id,
                )
            )
            if existing:
                abort(409, message="SKU already exists.")

        for key, value in product_data.items():
            if value is not None:
                setattr(product, key, value)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="SKU already exists.")

        return product

    @blp.response(204)
    def delete(self, product_id):
        product = db.session.scalar(
            db.select(Product).where(
                Product.id == product_id,
                Product.is_archived.is_(False),
            )
        )
        if product is None:
            abort(404, message="Product not found.")

        product.is_archived = True
        db.session.commit()
        return ""


@blp.route("/<int:product_id>/reserve")
class ProductReserve(MethodView):
    @blp.arguments(ProductReserveSchema, location="json")
    @blp.response(200, ProductSchema)
    def post(self, reserve_data, product_id):
        product = db.session.scalar(
            db.select(Product).where(
                Product.id == product_id,
                Product.is_archived.is_(False),
            )
        )
        if product is None:
            abort(404, message="Product not found.")

        quantity = reserve_data.get("qty") or reserve_data.get("quantity")
        if product.qty_in_stock < quantity:
            abort(409, message=f"Not enough stock. Available: {product.qty_in_stock}")

        product.qty_in_stock -= quantity
        db.session.commit()
        return product
