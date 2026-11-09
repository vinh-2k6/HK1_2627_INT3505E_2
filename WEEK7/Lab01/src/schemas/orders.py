from marshmallow import Schema, fields, validate


class OrderItemCreateSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))


class OrderCreateSchema(Schema):
    items = fields.List(
        fields.Nested(OrderItemCreateSchema),
        required=True,
        validate=validate.Length(min=1)
    )


class ProductInOrderSchema(Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    price_cents = fields.Int(dump_only=True)


class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(dump_only=True)
    product_id = fields.Int(dump_only=True)
    quantity = fields.Int(dump_only=True)
    unit_price = fields.Int(dump_only=True)
    product = fields.Nested(ProductInOrderSchema, dump_only=True)


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), dump_only=True)


class OrderListSchema(Schema):
    items = fields.List(fields.Nested(OrderSchema), dump_only=True)
    total = fields.Int(dump_only=True)
    page = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)


class OrderStatusUpdateSchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["pending", "processing", "completed", "cancelled"])
    )
