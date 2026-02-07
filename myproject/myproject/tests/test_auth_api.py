import pytest
from ninja.testing import TestClient

from myproject.urls import api


@pytest.fixture
def sync_client():
    return TestClient(api)


@pytest.mark.django_db(transaction=True)
def test_logout_clears_cookie(sync_client):
    """Test that logout endpoint clears the access_token cookie"""
    response = sync_client.post("/auth/logout")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Logged out"

    # delete_cookie は「空値 + max-age=0」で実現される
    cookies = response.cookies
    assert cookies["access_token"].value == ""
    assert cookies["access_token"]["max-age"] == 0


@pytest.mark.django_db(transaction=True)
def test_logout_is_idempotent(sync_client):
    """Test that calling logout multiple times always succeeds"""
    # 1回目のログアウト
    response = sync_client.post("/auth/logout")
    assert response.status_code == 200

    # 2回目のログアウト（Cookieが既にない状態でも成功する）
    response = sync_client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
