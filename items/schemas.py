from ninja import Schema

class ItemSchema(Schema):
    id: int
    name: str
    price:int

class ItemCreateSchema(Schema):
    name: str
    price: int
