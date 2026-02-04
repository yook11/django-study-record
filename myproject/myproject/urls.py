"""
URL configuration for myproject project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import include, path

# 👇 1. ここを変更！ (標準の NinjaAPI ではなく、拡張版の NinjaExtraAPI を使う)
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

# 👇 シンプル構成（パターン1）のルーター
from items.api import router as items_router

from . import views
from .auth_api import router as auth_router

# 👇 2. ここも変更！
api = NinjaExtraAPI()

# これで register_controllers が使えるようになります！
api.register_controllers(NinjaJWTDefaultController)

# ルーター登録
api.add_router("/items", items_router)
api.add_router("/auth", auth_router)

urlpatterns = [
    path("", lambda request: redirect("menu"), name="home"),
    path("admin/", admin.site.urls),
    path("exe01/", include("helloapp.urls")),
    path("exe02/", include("bookapp.urls")),
    path("menu/", views.MenuPageView.as_view(), name="menu"),
    path("exe03/", include("todoapp.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="todoapp/login.html"), name="login"),
    path("logout/", views.custom_logout_view, name="logout"),
    path("exe05/", include("appendixapp.urls")),
    path("api/", api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
