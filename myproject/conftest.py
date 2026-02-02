import pytest
from ninja.testing import TestAsyncClient
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth.models import User
from myproject.urls import api

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

@pytest.fixture
def auth_headers(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
async def async_client():
    async with TestAsyncClient(api) as client:
        yield client
