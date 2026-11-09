from marshmallow import Schema, fields

# Dinh nghia cau truc tra ve
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

# Dinh nghia cau truc khi khoi tao product
class ProductInSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
