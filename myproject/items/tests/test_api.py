import pytest

from items.models import Item


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_empty(async_client, auth_headers, db):
    """Test pagination with empty dataset"""
    response = await async_client.get("/items", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["items"] == []
    assert data["count"] == 0
    assert data["limit"] == 10
    assert data["offset"] == 0


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_with_data(async_client, auth_headers, db):
    """Test pagination with data - updated for new response structure"""
    await Item.objects.acreate(name="りんご", price=100)
    await Item.objects.acreate(name="みかん", price=80)

    response = await async_client.get("/items", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    # Updated: response is now paginated
    assert data["count"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "みかん"  # newest first (created second)
    assert data["limit"] == 10
    assert data["offset"] == 0


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_item_without_auth(async_client, db):
    response = await async_client.post("/items", json={"name": "バナナ", "price": 90})
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_item_with_auth(async_client, auth_headers, db):
    response = await async_client.post(
        "/items",
        json={"name": "バナナ", "price": 90},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "バナナ"
    assert data["price"] == 90


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_delete_item_without_auth(async_client, db):
    item = await Item.objects.acreate(name="バナナ", price=90)
    response = await async_client.delete(f"/items/{item.id}")
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_delete_item_with_auth(async_client, auth_headers, db):
    item = await Item.objects.acreate(name="削除対象", price=50)

    response = await async_client.delete(
        f"/items/{item.id}",
        headers=auth_headers,
    )
    assert response.status_code == 200

    exists = await Item.objects.filter(id=item.id).aexists()
    assert exists is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, price, expected_status",
    [
        ("普通の商品", 100, 200),  # ケース1: 普通のデータ
        ("無料の商品", 0, 200),  # ケース2: 0円 (境界値)
        ("高級な商品", 999999, 200),  # ケース3: 高額データ
        # ("マイナス", -100, 200),    # ケース4: マイナス (バリデーション未実装なら200になるはず)
    ],
)
async def test_create_item_variations(async_client, auth_headers, name, price, expected_status):
    """
    パラメタライズを使った多パターン検証
    """
    # 1. parametrizeで渡された変数(name, price)を使ってリクエスト
    response = await async_client.post(
        "/items", json={"name": name, "price": price}, headers=auth_headers
    )

    # 2. 期待するステータスコードと比較
    assert response.status_code == expected_status

    # 3. 成功(200)の場合は、保存されたデータの中身もチェック
    if expected_status == 200:
        data = response.json()
        assert data["name"] == name
        assert data["price"] == price


# Pagination-specific tests
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_pagination_structure(async_client, auth_headers, db):
    """Test that pagination response has correct structure"""
    response = await async_client.get("/items", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "count" in data
    assert "limit" in data
    assert "offset" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["count"], int)
    assert data["limit"] == 10  # Default
    assert data["offset"] == 0  # Default


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_pagination_with_data(async_client, auth_headers, db):
    """Test pagination with actual data"""
    # Create 15 items
    for i in range(15):
        await Item.objects.acreate(name=f"Item {i}", price=100 + i)

    # First page
    response = await async_client.get("/items?limit=5&offset=0", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data["items"]) == 5
    assert data["count"] == 15
    assert data["limit"] == 5
    assert data["offset"] == 0
    assert data["items"][0]["name"] == "Item 14"  # newest first

    # Second page
    response = await async_client.get("/items?limit=5&offset=5", headers=auth_headers)
    data = response.json()
    assert len(data["items"]) == 5
    assert data["count"] == 15
    assert data["items"][0]["name"] == "Item 9"  # offset 5 from newest

    # Last page (partial)
    response = await async_client.get("/items?limit=5&offset=10", headers=auth_headers)
    data = response.json()
    assert len(data["items"]) == 5
    assert data["count"] == 15
    assert data["items"][0]["name"] == "Item 4"  # offset 10 from newest


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_pagination_edge_cases(async_client, auth_headers, db):
    """Test pagination edge cases"""
    # Create 3 items
    await Item.objects.acreate(name="Item 1", price=100)
    await Item.objects.acreate(name="Item 2", price=200)
    await Item.objects.acreate(name="Item 3", price=300)

    # Offset beyond total count
    response = await async_client.get("/items?limit=10&offset=100", headers=auth_headers)
    data = response.json()
    assert len(data["items"]) == 0
    assert data["count"] == 3

    # Large limit (should be capped at 100 by validation)
    response = await async_client.get("/items?limit=100&offset=0", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["count"] == 3


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_invalid_parameters(async_client, auth_headers, db):
    """Test validation of pagination parameters"""
    # Negative limit (should fail validation)
    response = await async_client.get("/items?limit=-1", headers=auth_headers)
    assert response.status_code == 422  # Validation error

    # Negative offset (should fail validation)
    response = await async_client.get("/items?offset=-1", headers=auth_headers)
    assert response.status_code == 422

    # Limit > 100 (should fail validation)
    response = await async_client.get("/items?limit=101", headers=auth_headers)
    assert response.status_code == 422

    # Zero limit (should fail validation due to ge=1)
    response = await async_client.get("/items?limit=0", headers=auth_headers)
    assert response.status_code == 422
