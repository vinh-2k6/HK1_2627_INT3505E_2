from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.orm import selectinload

from src.extensions import db
from src.models import Order, OrderItem, Product
from src.schemas.orders import (
    OrderSchema,
    OrderCreateSchema,
    OrderListSchema,
    OrderStatusUpdateSchema,
)
from src.schemas.products import PaginationSchema

blp = Blueprint(
    "Orders",
    "orders",
    url_prefix="/api/v1/orders",
    description="Operations on orders and order items",
)


@blp.route("")
@blp.route("/")
class OrdersList(MethodView):
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, OrderListSchema)
    def get(self, pagination_data):
        page = pagination_data.get("page", 1)
        per_page = pagination_data.get("size") or pagination_data.get("per_page", 20)

        query = (
            db.select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .order_by(Order.id)
        )
        pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
        }

    @blp.arguments(OrderCreateSchema, location="json")
    @blp.response(201, OrderSchema)
    def post(self, order_data):
        order = Order(status="pending")
        db.session.add(order)

        for item_data in order_data["items"]:
            product = db.session.scalar(
                db.select(Product).where(
                    Product.id == item_data["product_id"],
                    Product.is_archived.is_(False),
                )
            )

            if product is None:
                db.session.rollback()
                abort(404, message=f"Product {item_data['product_id']} not found.")

            order_item = OrderItem(
                order=order,
                product=product,
                quantity=item_data["quantity"],
                unit_price=product.price_cents,
            )
            db.session.add(order_item)

        db.session.commit()
        return order


@blp.route("/<int:order_id>")
class OrderDetail(MethodView):
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        # Eager load items and products via selectinload to prevent N+1 query problem
        stmt = (
            db.select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.id == order_id)
        )
        order = db.session.scalar(stmt)

        if order is None:
            abort(404, message="Order not found.")

        return order

    @blp.arguments(OrderStatusUpdateSchema, location="json")
    @blp.response(200, OrderSchema)
    def patch(self, update_data, order_id):
        order = db.session.scalar(
            db.select(Order).where(Order.id == order_id)
        )
        if order is None:
            abort(404, message="Order not found.")

        order.status = update_data["status"]
        db.session.commit()
        return order
