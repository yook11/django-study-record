from ninja import Schema
from typing import List


class ItemSchema(Schema):
    id: int
    name: str
    price: int


class ItemCreateSchema(Schema):
    name: str
    price: int


class PaginatedItemsResponse(Schema):
    """
    Paginated response for items list.

    Attributes:
        items: List of items for the current page
        count: Total number of items across all pages
        limit: Number of items per page (requested)
        offset: Starting position for this page
    """
    items: List[ItemSchema]
    count: int
    limit: int
    offset: int
