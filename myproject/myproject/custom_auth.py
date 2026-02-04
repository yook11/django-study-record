from typing import Any, Optional

from django.http import HttpRequest
from ninja_extra.security import AsyncHttpBearer
from ninja_jwt.authentication import AsyncJWTBaseAuthentication


class AsyncJWTAuthWithCookie(AsyncJWTBaseAuthentication, AsyncHttpBearer):
    """
    AuthorizationヘッダーまたはCookieからJWTトークンを取得する認証クラス

    検索順序:
    1. Authorizationヘッダー（Bearer token）
    2. Cookieの"access_token"
    """

    async def __call__(self, request: HttpRequest) -> Optional[Any]:
        # 1. まずAuthorizationヘッダーを確認
        headers = request.headers
        auth_value = headers.get(self.header)

        if auth_value:
            parts = auth_value.split(" ")
            if parts[0].lower() == self.openapi_scheme:
                token = " ".join(parts[1:])
                return await self.authenticate(request, token)

        # 2. Authorizationヘッダーがない場合、Cookieから取得
        token = request.COOKIES.get("access_token")
        if token:
            return await self.authenticate(request, token)

        # 3. どちらもない場合はNone（認証失敗）
        return None

    async def authenticate(self, request: HttpRequest, token: str) -> Any:
        """トークンを検証してユーザーを返す"""
        return await self.async_jwt_authenticate(request, token)
