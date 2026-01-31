from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

# ==================================================
# メニュー画面用のビュー：継承元はTemplateView + LoginRequiredMixin
# ==================================================


class MenuPageView(LoginRequiredMixin, TemplateView):
    # 使用するテンプレートを指定
    template_name = "menu.html"


# ==================================================
# カスタムログアウトビュー：ログアウト後にメッセージを表示
# ==================================================


def custom_logout_view(request):
    """ログアウト処理を行い、メッセージを表示してログインページにリダイレクト"""
    logout(request)
    messages.success(request, "ログアウトしました")
    return redirect("login")
