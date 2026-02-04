from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Router

from myproject.custom_auth import AsyncJWTAuthWithCookie

from .models import Item
from .schemas import ItemCreateSchema, ItemSchema

router = Router()


@router.get("", response=List[ItemSchema], auth=AsyncJWTAuthWithCookie())
async def list_items(request):
    return [item async for item in Item.objects.all()]


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
