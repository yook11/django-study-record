from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Router, Query

from myproject.custom_auth import AsyncJWTAuthWithCookie

from .models import Item
from .schemas import ItemCreateSchema, ItemSchema, PaginatedItemsResponse

router = Router()


@router.get("", response=PaginatedItemsResponse, auth=AsyncJWTAuthWithCookie())
async def list_items(
    request,
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Starting position for pagination")
):
    """
    List items with pagination support.

    Query Parameters:
        - limit: Number of items to return (default: 10, max: 100)
        - offset: Number of items to skip (default: 0)

    Returns:
        PaginatedItemsResponse with items, count, limit, and offset
    """
    # Get total count (native async - Django 6.0+)
    total_count = await Item.objects.acount()

    # Get paginated items (native async iteration with slicing)
    queryset = Item.objects.order_by('-id')[offset:offset + limit]
    items = [item async for item in queryset]

    return {
        "items": items,
        "count": total_count,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{item_id}", response=ItemSchema, auth=AsyncJWTAuthWithCookie())
async def get_item(request, item_id: int):
    return await aget_object_or_404(Item, id=item_id)


@router.post("", response=ItemSchema, auth=AsyncJWTAuthWithCookie())
async def create_item(request, data: ItemCreateSchema):
    return await Item.objects.acreate(
        name=data.name,
        price=data.price,
    )


@router.put("/{item_id}", response=ItemSchema, auth=AsyncJWTAuthWithCookie())
async def update_item(request, item_id: int, data: ItemCreateSchema):
    item = await aget_object_or_404(Item, id=item_id)
    item.name = data.name
    item.price = data.price
    await item.asave()
    return item


@router.delete("/{item_id}", auth=AsyncJWTAuthWithCookie())
async def delete_item(request, item_id: int):
    item = await aget_object_or_404(Item, id=item_id)
    await item.adelete()
    return {"success": True}
