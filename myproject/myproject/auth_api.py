from django.conf import settings as django_settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from ninja import Router, Schema
from ninja.responses import Response
from ninja_jwt.tokens import RefreshToken

router = Router()


# 👇 1. 受け取るデータの形（入力スキーマ）を定義する
class LoginInput(Schema):
    username: str
    password: str


# 👇 2. async を外して def にする（DB操作があるため）
# 👇 3. 引数に data: LoginInput を指定する
@router.post("/login")
def login(request, data: LoginInput):
    # data.username, data.password でアクセスする
    user = authenticate(username=data.username, password=data.password)

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # ボディにはトークンを含めなくても良いが、デバッグ用に含めてもOK
    response = Response(
        {
            "message": "Login successful",
            # "access": access_token, # Cookieにあるのでボディからは消してもOK
        }
    )

    jwt_settings = django_settings.NINJA_JWT
    response.set_cookie(
        key=jwt_settings["AUTH_COOKIE"],
        value=access_token,
        httponly=jwt_settings["AUTH_COOKIE_HTTP_ONLY"],
        samesite=jwt_settings["AUTH_COOKIE_SAMESITE"],
        secure=jwt_settings["AUTH_COOKIE_SECURE"],
        domain=jwt_settings["AUTH_COOKIE_DOMAIN"],
        max_age=int(jwt_settings["ACCESS_TOKEN_LIFETIME"].total_seconds()),
    )

    return response


@router.post("/logout")
def logout(request, response: HttpResponse):
    jwt_settings = django_settings.NINJA_JWT
    response.delete_cookie(
        jwt_settings["AUTH_COOKIE"],
        domain=jwt_settings["AUTH_COOKIE_DOMAIN"],
        samesite=jwt_settings["AUTH_COOKIE_SAMESITE"],
    )
    return {"message": "Logged out"}
