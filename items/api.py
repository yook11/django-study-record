from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Item
from .schemas import ItemSchema, ItemCreateSchema

router = Router()

@router.get("", response=List[ItemSchema])
def list_items(request):
    return Item.objects.all()

@router.get("/{item_id}", response=ItemSchema)
def get_item(request, item_id: int):
    item = get_object_or_404(Item, id = item_id)
    return item

@router.post("", response=ItemSchema)
def create_item(request, data: ItemCreateSchema):
    item = Item.objects.create(
        name=data.name,
        price=data.price,
    )
    return item

@router.put("/{item_id}", response=ItemSchema)
def update_item(request, item_id: int, data: ItemCreateSchema):
    item = get_object_or_404(Item, id=item_id)
    item.name = data.name
    item.price = data.price
    item.save()
    return item

@router.delete("/{item_id}", response=ItemSchema)
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"success": True}