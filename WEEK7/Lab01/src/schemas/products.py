from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))
    is_archived = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductInSchema(Schema):
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))


class ProductPatchSchema(Schema):
    sku = fields.Str(validate=validate.Length(min=3, max=32))
    name = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(validate=validate.Range(min=0))
    qty_in_stock = fields.Int(validate=validate.Range(min=0))


class ProductReserveSchema(Schema):
    qty = fields.Int(validate=validate.Range(min=1))
    quantity = fields.Int(validate=validate.Range(min=1))

    @validates_schema
    def validate_quantity_present(self, data, **kwargs):
        if "qty" not in data and "quantity" not in data:
            raise ValidationError("Either 'qty' or 'quantity' is required.")


class ProductListSchema(Schema):
    items = fields.List(fields.Nested(ProductSchema), dump_only=True)
    total = fields.Int(dump_only=True)
    page = fields.Int(dump_only=True)
    size = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)


class PaginationSchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    size = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
