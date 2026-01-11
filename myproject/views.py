from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# ==================================================
# メニュー画面用のビュー：継承元はTemplateView + LoginRequiredMixin
# ==================================================

class MenuPageView(LoginRequiredMixin,TemplateView):
    # 使用するテンプレートを指定
    template_name = 'menu.html'