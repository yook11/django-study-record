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

    # Cookieにアクセストークンを設定（完璧です！）
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,  # 開発環境用
        max_age=900,  # 15分
    )

    return response


@router.post("/logout")
def logout(request, response: HttpResponse):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
