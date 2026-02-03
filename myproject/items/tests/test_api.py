import pytest

from items.models import Item


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_empty(async_client, db):
    response = await async_client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_list_items_with_data(async_client, db):
    await Item.objects.acreate(name="りんご", price=100)
    await Item.objects.acreate(name="みかん", price=80)

    response = await async_client.get("/items")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "りんご"


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
